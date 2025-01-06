from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import FaSequence, Annotation
from django.urls import reverse
from .forms import FaSequenceForm
from django.contrib import messages

def home(request):
    #homepage avec toute les sequences 
    sequences = FaSequence.objects.all()
    return render(request, 'genhome/index.html', {'sequences':sequences})


def annotate_sequence(request, sequence_id):
    sequence = get_object_or_404(FaSequence, id=sequence_id)

    if request.method == 'POST':
        annotation_content = request.POST.get('annotation')
        if annotation_content:
            Annotation.objects.create(sequence=sequence, content=annotation_content)
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
    if request.method == 'POST':
        form = FaSequenceForm(request.POST)
        #vérification si la séquence valide
        seq = request.POST.get('sequence')  
        if not is_dna(seq):  
            messages.error(request, "Veuillez rentrez une sequence ADN valide")
            return render(request, 'genhome/add_sequence.html', {'form': form})
        # Si oui enregistre la nouvelle sequence avec un nouvel id 
        if form.is_valid():
            fa_sequence = form.save()  
            return redirect('annotate_sequence', sequence_id=fa_sequence.id)
    else:
        form = FaSequenceForm()
    return render(request, 'genhome/add_sequence.html', {'form': form})


def is_dna(seq):
    for nucleotide in seq:
        if nucleotide not in ['A', 'T', 'C', 'G']:
            return False
    return True