from django.shortcuts import render
from annotation.models import Genome
from genhome.models import FaSequence
from search.forms import SequenceSearchForm

def search_sequences(request):
    form = SequenceSearchForm(request.GET or None)
    results = []
    if form.is_valid():
        genome_name = form.cleaned_data.get('species', '')
        sequence = form.cleaned_data.get('sequence', '')
        
        if genome_name:
            genome = Genome.objects.filter(name__icontains=genome_name).first()
            if genome:
                results = FaSequence.objects.filter(genome=genome)
        elif sequence:
            results = FaSequence.objects.filter(sequence__icontains=sequence)

    return render(request, 'search/search_results.html', {'form': form, 'results': results})

