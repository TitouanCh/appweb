from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404
from search.models import Genome, GeneProtein
from search.forms import SequenceSearchForm

def search_sequences(request):
    form = SequenceSearchForm(request.GET or None)
    results = []
    if form.is_valid():
        sequence = form.cleaned_data['sequence']
        species = form.cleaned_data['species']
        output_type = form.cleaned_data['output_type']
        
        if output_type == 'genome':
            results = Genome.objects.all()
            if sequence:
                results = results.filter(sequence__icontains=sequence)
            if species:
                results = results.filter(species__icontains=species)
        elif output_type == 'gene_protein':
            results = GeneProtein.objects.all()
            if sequence:
                results = results.filter(sequence__icontains=sequence)
            if species:
                results = results.filter(genome__species__icontains=species)

    return render(request, 'search/search_results.html', {'form': form, 'results': results})

def view_detail(request, id):
    genome = get_object_or_404(Genome, id=id)
    return render(request, 'genome_detail.html', {'genome': genome})
