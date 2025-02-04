from django.shortcuts import redirect, render
from .models import Database
from genhome.models import FaSequence


def database_list(request):
    databases = Database.objects.all()
    if request.method == "POST":
        return redirect('blast_request')
    return render(request, "blast_request.html", {"databases": databases})


def blast_request_view(request):
    """
    Vue permettant d'accéder aux bases de données externes et de sélectionner des séquences locales ou saisies.
    """
    # Récupération des bases de données disponibles
    databases = Database.objects.all()

    # Initialiser les variables
    sequences = FaSequence.objects.none()  # Aucun accès par défaut
    error_message = None
    redirect_url = None
    uniprot_sequence = None

    # Charger les séquences si l'utilisateur est connecté
    if request.user.is_authenticated:
        sequences = FaSequence.objects.all()  # Charger toutes les séquences locales
        print(f"Séquences disponibles pour {request.user.email} : {[seq.sequence[:30] for seq in sequences]}")
    else:
        print("Utilisateur non connecté : pas de séquences disponibles.")

    # Si une requête POST est envoyée
    if request.method == 'POST':
        # Récupérer les données du formulaire
        selected_db_id = request.POST.get('database')
        sequence_id = request.POST.get('sequence_id')  # Séquence locale sélectionnée
        sequence_input = request.POST.get('sequence', '').strip()  # Séquence saisie manuellement

        # Vérifier si une séquence a été sélectionnée ou saisie
        if sequence_id:
            try:
                selected_sequence = FaSequence.objects.get(id=sequence_id)
                sequence = selected_sequence.sequence
            except FaSequence.DoesNotExist:
                error_message = "Séquence sélectionnée invalide."
        else:
            sequence = sequence_input

        # Valider la séquence saisie
        if sequence:
            if all(base in "ATCGUatcgu" for base in sequence):  # Nucléotidique
                tool = "blastn"
            elif all(aa in "ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy" for aa in sequence):  # Peptidique
                tool = "blastp"
            else:
                error_message = "La séquence entrée est invalide. Veuillez vérifier votre saisie."

            # Récupérer la base de données sélectionnée
            if not error_message:
                try:
                    selected_db = Database.objects.get(id=selected_db_id)
                    if "uniprot" in selected_db.url.lower():
                        uniprot_sequence = sequence  # Pour UniProt
                    elif tool == "blastn" and selected_db.blastn_url:
                        redirect_url = f"{selected_db.blastn_url}{sequence}"
                    elif tool == "blastp" and selected_db.blastp_url:
                        redirect_url = f"{selected_db.blastp_url}{sequence}"
                    else:
                        error_message = "La base de données sélectionnée ne supporte pas ce type de séquence."
                except Database.DoesNotExist:
                    error_message = "Base de données sélectionnée invalide."
        else:
            error_message = "Aucune séquence n'a été saisie ou sélectionnée."

    # Rendre la page avec toutes les séquences et bases de données
    return render(request, 'blast_request.html', {
        'databases': databases,
        'sequences': sequences,
        'redirect_url': redirect_url,
        'error_message': error_message,
        'uniprot_sequence': uniprot_sequence,
    })
