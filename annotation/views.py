from django.http import HttpResponseForbidden,HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import Annotation,Feature,Genome
from django.urls import reverse
from .forms import FaSequenceForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from genhome.models import FaSequence
import json

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
            existing_genome = form.cleaned_data['existing_genome']
            new_genome_name = form.cleaned_data['new_genome']
            if new_genome_name:
                genome_, created = Genome.objects.get_or_create(name=new_genome_name)
            else:
                genome_= existing_genome
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
                    identifiant=ids[i],
                    genome=genome_
                )
                new_sequence.save()
                new_sequence_ids.append(new_sequence.id) 
                #Enregistrer les features de la sequence : 
                for feature in features_list: 
                    if feature=='description' :
                        if annotations[i][feature]!='non defini':
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
    for nucleotide in seq.strip():
        if nucleotide not in ['A','B', 'R','N', 'D', 'C', 'Q', 'E','G','H', 'I','L', 'K', 'M', 'F', 'P','S', 'T', 'W', 'Y', 'V', 'U','X', 'O','Z' ] :
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
                if annotationsbyseq!=[] : 
                    sequences.append(s)
                    s=''
                if len(line.split(features_list[0])[0].split('cds'))>1 :
                        id.append(line.split(features_list[0])[0].split('cds')[0].strip()[1:])
                elif len(line.split(features_list[0])[0].split('pep'))>1 :
                        id.append(line.split(features_list[0])[0].split('pep')[0].strip()[1:])
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
    Genome.objects.all().delete()
    return HttpResponse("Toutes les séquences ont été supprimées.")


def download_sequence_with_annotations(request, sequence_id):
    sequence = get_object_or_404(FaSequence, id=sequence_id)
    annotations = sequence.annotations.all()

    # Créer le contenu du fichier
    file_content = 'ID sequence '+str(sequence_id)+'\n'
    file_content += "Statut: "+str(sequence.get_status_display())+"\n"
    file_content += "Annotations:\n"
    
    if annotations.exists():
        for annotation in annotations:
            file_content += (
                f"- {annotation.content} (Ajoutée le {annotation.created_at.strftime('%d-%m-%Y %H:%M')} "
                f"par {annotation.owner.email})\n"
            )
    else:
        file_content += "Aucune annotation disponible.\n"

    file_content += " Séquence:\n"+str(sequence.sequence)+"\n"

    # Générer le fichier pour le téléchargement
    response = HttpResponse(file_content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=sequence_{sequence_id}_with_annotations.txt'
    return response


<<<<<<< HEAD
def genome_sequences(request, genome_id):
    genome = get_object_or_404(Genome, id=genome_id)
    sequences = FaSequence.objects.filter(genome=genome) [:20]

    annotated_sequences_count = Annotation.objects.filter(sequence__genome=genome).values('sequence').distinct().count()
    total_sequences_count = sequences.count()
        # Ajouter une information sur chaque séquence pour savoir si elle est annotée ou non
    for sequence in sequences:
        sequence.is_annotated = Annotation.objects.filter(sequence=sequence).exists()


    return render(request, 'annotation/genome_sequences.html', {
        'genome': genome,
        'sequences': sequences,
        'annotated_sequences_count': annotated_sequences_count,
        'total_sequences_count': total_sequences_count,
    })


def import_sequences(fasta_file, status, owner, new_genome_name=None, existing_genome=None):
    sequences = []
    ids = []
    annotations = {}
    try:
        # Extraction des séquences et annotations
        annotations, sequences, ids = extract_sequence_from_fasta(fasta_file)
    except ValidationError as e:
        raise ValidationError("Le fichier FASTA est invalide. Erreur : " + str(e))

    if new_genome_name:
        genome_, created = Genome.objects.get_or_create(name=new_genome_name)
    else:
        genome_ = existing_genome
    # Enregistrer les séquences
    invalid_sequences = []
    new_sequence_ids = []
    for i, sequence in enumerate(sequences):
        if not is_dna(sequence) and not is_prot(sequence):
            invalid_sequences.append(i)
            continue

        new_sequence = FaSequence(
            status=status,
            sequence=sequence,
            owner=owner,
            identifiant=ids[i],
            genome=genome_
        )
        new_sequence.save()
        new_sequence_ids.append(new_sequence.id)

        # Enregistrer les annotations
        for feature in annotations[i]:
            if feature == 'description' and annotations[i][feature] != 'non defini':
                new_annotation = Annotation(
                    sequence=new_sequence,
                    owner=owner,
                    content=annotations[i][feature]
                )
                new_annotation.save()

    return new_sequence_ids, invalid_sequences
=======
def validate_annotations(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to verify annotations.")
    
    if not request.user.owns_sequence():
        return HttpResponseForbidden("You must own at least one sequence to verify annotations.")
    

    sequences = request.user.get_owned_sequences()
    annotations = Annotation.objects.filter(sequence__in=sequences)

    return render(
        request, 
        'annotation/validate.html', 
        {'sequences': sequences,'annotations': annotations}
    )


def process_annotations(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to verify annotations.")
    
    if not request.user.owns_sequence():
        return HttpResponseForbidden("You must own at least one sequence to verify annotations.")
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            request_id = data.get('request_id', None)
            action_type = data.get('type', None)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        annotation = Annotation.objects.get(id=request_id)
        owned_sequences = request.user.get_owned_sequences()

        if not owned_sequences.filter(id=annotation.sequence.id).exists(): # check if the user is validating a annotation from one of his sequence and not someone elses
            return HttpResponseForbidden("This is not your sequence!")

        if action_type == "accept":
            annotation.accept()
            return JsonResponse({'request_id': request_id, 'type': action_type, 'display': 'Acceptée'})
        elif action_type == "deny":
            annotation.deny()
            return JsonResponse({'request_id': request_id, 'type': action_type, 'display': 'Refusée'})

        return JsonResponse({'error': 'Invalid type'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
>>>>>>> main
