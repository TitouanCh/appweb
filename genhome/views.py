from django.http import HttpResponseForbidden
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import FaSequence, Annotation
from django.urls import reverse
from .forms import FaSequenceForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404

def home(request):
    #homepage avec toute les sequences 
    sequences = FaSequence.objects.all()
    return render(request, 'genhome/index.html', {'sequences':sequences})


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
        'genhome/annotate_sequence.html', 
        {'sequence': sequence, 'annotations': annotations}
    )

def delete_annotation(request, annotation_id):
    annotation = get_object_or_404(Annotation, id=annotation_id)
    annotation.delete()
    return redirect(reverse('annotate_sequence', args=[annotation.sequence.id]))


def add_sequence(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged to add a new sequence.")

    if request.method == 'POST':
        form = FaSequenceForm(request.POST, request.FILES)
        if not form.is_valid():
            print(form.errors)  # Affichez les erreurs dans la console
        # Si oui enregistre la nouvelle sequence avec un nouvel id 
        if form.is_valid():
            fasta_file = request.FILES['sequence_file']
            sequence = extract_sequence_from_fasta(fasta_file)
                    #vérification si la séquence valide
            if not is_dna(sequence):  
                messages.error(request, "Veuillez rentrez une sequence ADN valide")
                return render(request, 'genhome/add_sequence.html', {'form': form})
        # Si oui enregistre la nouvelle sequence avec un nouvel id 
            # Enregistrer la nouvelle séquence dans la base de données
            print('c')
            new_sequence = FaSequence(
                status=form.cleaned_data['status'],
                sequence=sequence,
                owner=request.user
            )
            fa_sequence = new_sequence.save() 
            return redirect('annotate_sequence', sequence_id=new_sequence.id)
    else:
        form = FaSequenceForm()
    return render(request, 'genhome/add_sequence.html', {'form': form})


def is_dna(seq):
    for nucleotide in seq:
        if nucleotide not in ['A', 'T', 'C', 'G']:
            return False
    return True


def extract_sequence_from_fasta(file):
    """Extrait la séquence d'un fichier FASTA."""
    try:
        # Lire le contenu du fichier FASTA
        content = file.read().decode('utf-8')
        
        # Séparer par les lignes et ignorer les lignes qui commencent par '>'
        lines = content.splitlines()
        print(lines)
        sequence = ''.join(line for line in lines if not line.startswith('>'))
        print(sequence)
        return sequence
    except Exception as e:
        raise ValidationError(f"Erreur lors de la lecture du fichier FASTA : {e}")
