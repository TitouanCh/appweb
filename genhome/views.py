from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import FaSequence, Annotation

def home(request):
    return render(request, 'genhome/index.html', {})


def annotate_sequence(request, sequence_id):
    sequence = get_object_or_404(FaSequence, id=sequence_id)

    if request.method == 'POST':
        annotation = request.POST.get('annotation')
    sequence = get_object_or_404(FaSequence, id=sequence_id)
    
    return render(request, 'genhome/annotate_sequence.html', {'sequence': sequence})
