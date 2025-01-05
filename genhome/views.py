from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import FaSequence, Annotation

def home(request):
    return render(request, 'genhome/index.html', {})

def annotate_sequence(request, sequence_id):
    sequence = get_object_or_404(FaSequence, id=sequence_id)

    if request.method == 'POST':
        annotation_content = request.POST.get('annotation')
        if annotation_content:  # Vérifie si une annotation a été soumise
            Annotation.objects.create(sequence=sequence, content=annotation_content)
            return redirect('annotate_sequence', sequence_id=sequence.id)

    # Récupère toutes les annotations associées à la séquence
    annotations = sequence.annotations.all()

    return render(
        request, 
        'genhome/annotate_sequence.html', 
        {'sequence': sequence, 'annotations': annotations}
    )