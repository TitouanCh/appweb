from django.shortcuts import redirect, render
from .models import BioDatabase
from genhome.models import FaSequence


def database_list(request):
    databases = BioDatabase.objects.all()
    if request.method == "POST":
        return redirect('blast_request')
    return render(request, "blast_request.html", {"databases": databases})


def blast_request_view(request):
    if not request.user.is_authenticated:
        request.session['next'] = request.get_full_path()
        return redirect('/login/')

    databases = BioDatabase.objects.all()
    sequences = FaSequence.objects.all()

    error_message = None
    redirect_url = None
    selected_db_name = None  # Nouvelle variable pour stocker le nom de la base de données

    if request.method == 'POST':
        selected_db_id = request.POST.get('database')
        sequence_id = request.POST.get('sequence_id')
        sequence_input = request.POST.get('sequence', '').strip()

        sequence = None
        if sequence_id:
            try:
                selected_sequence = FaSequence.objects.get(id=sequence_id)
                sequence = selected_sequence.sequence
            except FaSequence.DoesNotExist:
                error_message = "Séquence sélectionnée invalide."
        elif sequence_input:
            sequence = sequence_input

        if sequence:
            if all(base in "ATCGUatcgu" for base in sequence):
                tool = "blastn"
            elif all(aa in "ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy" for aa in sequence):
                tool = "blastp"
            else:
                error_message = "La séquence entrée est invalide."
                tool = None

            if not error_message:
                try:
                    selected_db = BioDatabase.objects.get(id=selected_db_id)
                    selected_db_name = selected_db.name  # Récupérer le nom de la base de données
                    if "uniprot" in selected_db.url.lower():
                        if tool == "blastp":
                            redirect_url = f"https://www.uniprot.org/blast/?sequence={sequence}"
                        else:
                            error_message = "UniProt ne supporte que les séquences peptidiques (BlastP)."
                    elif tool == "blastn" and selected_db.blastn_url:
                        redirect_url = f"{selected_db.blastn_url}{sequence}"
                    elif tool == "blastp" and selected_db.blastp_url:
                        redirect_url = f"{selected_db.blastp_url}{sequence}"
                    else:
                        error_message = "La base de données sélectionnée ne supporte pas ce type de séquence."
                except BioDatabase.DoesNotExist:
                    error_message = "Base de données sélectionnée invalide."
        else:
            error_message = "Aucune séquence n'a été saisie ou sélectionnée."

    return render(request, 'blast_request.html', {
        'databases': databases,
        'sequences': sequences,
        'redirect_url': redirect_url,
        'error_message': error_message,
        'selected_db_name': selected_db_name,  # Ajout au contexte
    })