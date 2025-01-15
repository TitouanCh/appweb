from django.http import HttpResponseForbidden
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import Annotation
from django.urls import reverse
from .forms import FaSequenceForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from genhome.models import FaSequence

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

    return render(
        request, 
        'annotation/annotate_sequence.html', 
        {'sequence': sequence, 'annotations': annotations}
    )


def simple_view(request, sequence_id):
    sequence = get_object_or_404(FaSequence, id=sequence_id)
    annotations = sequence.annotations.all()
    return render(
        request, 
        'annotation/simple_view.html', 
        {'sequence': sequence,'annotations': annotations}
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
                annotations, sequences = extract_sequence_from_fasta(fasta_file)
            except ValidationError as e:
                messages.error(request, str(e))
                return render(request, 'annotation/add_sequence.html', {'form': form})
            
            invalid_sequences = []
            new_sequence_ids = []
            for i, sequence in enumerate(sequences):
                if not is_dna(sequence):
                    invalid_sequences.append(annotations[i])
                    continue  #Passer la sequence si ce n'est pas de l'adn 

                # Enregistrer chaque séquence valide dans la base de données
                new_sequence = FaSequence(
                    status=form.cleaned_data['status'],
                    sequence=sequence
                )
                new_sequence.save()
                new_sequence_ids.append(new_sequence.id) 
            # messages utilisateurs  
            if invalid_sequences:
                messages.warning(request, f"attention il y a des sequences invalide apres header  : {', '.join(invalid_sequences)}")
            if new_sequence_ids:
                messages.success(request, f"{len(new_sequence_ids)} séquences ajoutées.")
            
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
        if nucleotide not in ['A', 'T', 'C', 'G']:
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
        sequences=[]
        annotations=[]
        s=''
        for line in lines : 
            if line.startswith('>'): 
                if annotations!=[] : 
                    sequences.append(s)
                    s=''
                annotations.append(line.strip())
            else : 
                s=s+line.strip()
        sequences.append(s) # on oublie pas la derniere sequence
        return annotations,sequences
    except Exception as e:
        print(e)
        raise ValidationError('Erreur de lecture du fichier ')