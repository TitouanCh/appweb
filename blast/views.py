from django.shortcuts import render, get_object_or_404
from genhome.models import FaSequence  # Import FaSequence model
from .forms import SequenceForm  # Import the custom form
import subprocess

def run_blast(sequence):
    """Execute BLAST using the given sequence."""
    with open("query.fasta", "w") as file:
        file.write(f">Query\n{sequence}")

    result = subprocess.run(
        ["blastn", "-query", "query.fasta", "-db", "nt", "-outfmt", "6"],
        capture_output=True,
        text=True
    )
    return result.stdout

def blast_view(request, sequence_id=None):
    """View to display sequences and handle BLAST search."""
    sequences = FaSequence.objects.all()  # Fetch all sequences
    selected_sequence = None
    result = None

    if sequence_id:
        selected_sequence = get_object_or_404(FaSequence, id=sequence_id)
        result = run_blast(selected_sequence.sequence)

    return render(request, "blast/blast_form.html", {
        "sequences": sequences,
        "selected_sequence": selected_sequence,
        "result": result,
        "form": SequenceForm() if not sequence_id else None
    })
