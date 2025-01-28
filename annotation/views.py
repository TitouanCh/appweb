from django.http import HttpResponseForbidden,HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import Annotation,Feature
from django.urls import reverse
from .forms import FaSequenceForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from genhome.models import FaSequence


features_list=['chromosome','gene','transcript','gene_biotype','transcript_biotype','gene_symbol','description']

def annotate_sequence(request, sequence_id):
    sequence = get_object_or_404(FaSequence, id=sequence_id)

    if not request.user.is_authenticated: # TODO: Checker les droits de l'utilisateur aussi
        return HttpResponseForbidden("You must be logged in to create an annotation.")

    if request.method == 'POST':
        annotation_content = request.POST.get('annotation')
        if annotation_content:
            Annotation.objects.create(
                sequence=sequence,
                content=annotation_content,
                owner=request.user
            )
            return redirect('annotate_sequence', sequence_id=sequence.id)
    annotations = sequence.annotations.all()
    features=sequence.feature.all()

    return render(
        request, 
        'annotation/annotate_sequence.html', 
        {'sequence': sequence, 'annotations': annotations,'features' : features}
    )


def simple_view(request, sequence_id):
    sequence = get_object_or_404(FaSequence, id=sequence_id)
    annotations = sequence.annotations.all() # Transformation des features en liste
    features=sequence.feature.all()
    related_sequences = []
    print(sequence.identifiant)
    if sequence.identifiant not in ["Genome", "Non defini"]:
        related_sequences = FaSequence.objects.filter(
            identifiant=sequence.identifiant
        ).exclude(id=sequence.id)
        print(sequence)
    return render(
        request, 
        'annotation/simple_view.html', 
        {'sequence': sequence,'annotations': annotations,'features' : features,'related_sequences': related_sequences}
    )



def delete_annotation(request, annotation_id):
    annotation = get_object_or_404(Annotation, id=annotation_id)
    annotation.delete()
    return redirect(reverse('annotate_sequence', args=[annotation.sequence.id]))


def add_sequence(request):
    if request.method == 'POST':
        form = FaSequenceForm(request.POST, request.FILES)
        if not form.is_valid():
            print(form.errors)  # Affichez les erreurs dans la console
        
        if form.is_valid():
            fasta_file = request.FILES['sequence_file']
            try:
                annotations, sequences,ids = extract_sequence_from_fasta(fasta_file)
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, 'annotation/add_sequence.html', {'form': form})
            
            invalid_sequences = []
            new_sequence_ids = []
            for i, sequence in enumerate(sequences):
                if not is_dna(sequence):
                    if not is_prot(sequence) : 
                        invalid_sequences.append(i)
                        continue  #Passer la sequence si ce n'est pas de l'adn ou du prot
                # Enregistrer chaque séquence valide dans la base de données
                new_sequence = FaSequence(
                    status=form.cleaned_data['status'],
                    sequence=sequence,
                    #features_val=('|').join([annotations[i][key] for key in annotations[i]]),
                    owner=request.user,
                    identifiant=ids[i]
                )
                new_sequence.save()
                new_sequence_ids.append(new_sequence.id) 
                #Enregistrer les features de la sequence : 
                for feature in features_list: 
                    if feature=='description' :
                        new_annotations=Annotation(sequence=new_sequence,
                                                   owner=request.user,
                                                   content=annotations[i][feature]
                                                   )
                        new_annotations.save()
                    else : 
                        new_feature=Feature(sequence=new_sequence,
                                            status=feature,
                                            value=annotations[i][feature],
                                            owner=request.user)
                        new_feature.save()
            # messages utilisateurs  
            if invalid_sequences:
                messages.warning(request, f"attention il y a des sequences invalide apres header  : {', '.join(annotations[i])}")
            #if new_sequence_ids:
                #messages.success(request, f"{len(new_sequence_ids)} séquences ajoutées.")
            
            # Rediriger vers la page d'annotation de la premiere sequence ajoutée
            if new_sequence_ids:
                return redirect('annotate_sequence', sequence_id=new_sequence_ids[0])
            else:
                return render(request, 'annotation/add_sequence.html', {'form': form})

    else:
        form = FaSequenceForm()
    return render(request, 'annotation/add_sequence.html', {'form': form})


def is_dna(seq):
    for nucleotide in seq:
        if nucleotide not in ['A', 'T', 'C', 'G','M','R','W','S','Y','K','V','H','B','D','N']:
            return False
    return True

def is_prot(seq) : 
    for nucleotide in seq:
        if nucleotide not in ['A', 'R',  'N',  'D',  'C', 'Q', 'E','G',  'H', 'I', 'L', 'K', 'M', 'F', 'P',  'S', 'T',  'W',  'Y',  'V',  'U',  'O'  ] :
            return False
    return True


def extract_sequence_from_fasta(file):
    try:
        # Lire le contenu du fichier FASTA
        content = file.read().decode('utf-8')
        # Séparer par les lignes et ignorer les lignes qui commencent par '>'
        lines = content.splitlines()
        sequences=[]    # liste de sequences
        annotationsbyseq=[] # liste de dictionnaires de features pour chaque sequence
        annotations={}  # dictionnaire avec features : features values pour chaque features défini
        id=[]
        #print(features_list)
        s=''
        for line in lines : 
            if line.startswith('>'): 
                #print('c')
                if annotationsbyseq!=[] : 
                    sequences.append(s)
                    s=''
                if len(line.split(features_list[0])[0].split('cds'))>1 :
                        id.append(line.split(features_list[0])[0].split('cds')[0].strip())[1:]
                elif len(line.split(features_list[0])[0].split('pep'))>1 :
                        id.append(line.split(features_list[0])[0].split('pep')[0].strip())[1:]
                else : 
                    id.append('Genome')
                for f in features_list :
                    if len(line.split(f+':'))>1 : 
                        if f=='description' : 
                            annotations[f]=line.split(f+':')[1].strip()
                        else :
                            annotations[f]=line.split(f+':')[1].split(' ')[0].strip()
                    else : 
                        annotations[f]='non defini'
                annotationsbyseq.append(annotations)
            else : 
                s=s+line.strip()
        sequences.append(s) # on oublie pas la derniere sequence
        #print(len(sequences),len(annotationsbyseq))
        return annotationsbyseq,sequences,id
    except Exception as e:
        print(e)
        raise ValidationError('Erreur de lecture du fichier ')
    

#Bouton Rouge attention 
def delete_all_sequences(request):
    FaSequence.objects.all().delete()
    return HttpResponse("Toutes les séquences ont été supprimées.")