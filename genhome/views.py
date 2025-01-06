from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import FaSequence, Annotation
from django.shortcuts import render, get_object_or_404
from .models import Genome, GeneProtein
from .forms import SequenceSearchForm

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
    
    return render(request, 'search_results.html', {'form': form, 'results': results})
def view_detail(request, id):
    genome = get_object_or_404(Genome, id=id)
    return render(request, 'genome_detail.html', {'genome': genome})
