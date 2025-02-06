from django.shortcuts import redirect, render
from .models import BioDatabase
from genhome.models import FaSequence


def database_list(request):
    databases = BioDatabase.objects.all()
    if request.method == "POST":
        return redirect('blast_request')
    return render(request, "blast_request.html", {"databases": databases})


def blast_request_view(request):
    """
    Vue permettant d'accéder aux bases de données externes et de sélectionner des séquences locales ou saisies.
    """
    # Vérification si l'utilisateur est connecté
    if not request.user.is_authenticated:
        print("Utilisateur non connecté : redirection vers la page de connexion.")
        request.session['next'] = request.path  # Stocke l'URL actuelle dans la session
        return redirect('/login/')


    # L'utilisateur est maintenant connecté, on charge les bases de données et séquences
    databases = BioDatabase.objects.all()
    sequences = FaSequence.objects.all()  # On charge directement toutes les séquences locales

    print(f"Séquences disponibles pour {request.user.email} : {[seq.sequence[:30] for seq in sequences]}")

    # Initialisation des variables pour gérer la requête
    error_message = None
    redirect_url = None

    # Traitement de la requête POST (si soumission du formulaire)
    if request.method == 'POST':
        selected_db_id = request.POST.get('database')
        sequence_id = request.POST.get('sequence_id')  # Séquence locale sélectionnée
        sequence_input = request.POST.get('sequence', '').strip()  # Séquence saisie manuellement

        # Vérifier si une séquence a été sélectionnée ou saisie
        sequence = None
        if sequence_id:
            try:
                selected_sequence = FaSequence.objects.get(id=sequence_id)
                sequence = selected_sequence.sequence
            except FaSequence.DoesNotExist:
                error_message = "Séquence sélectionnée invalide."
        elif sequence_input:
            sequence = sequence_input

        # Valider la séquence saisie
        if sequence:
            if all(base in "ATCGUatcgu" for base in sequence):  # Séquence nucléotidique
                tool = "blastn"
            elif all(aa in "ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy" for aa in sequence):  # Séquence peptidique
                tool = "blastp"
            else:
                error_message = "La séquence entrée est invalide. Veuillez vérifier votre saisie."
                tool = None

            # Récupérer la base de données sélectionnée et gérer la redirection
            if not error_message:
                try:
                    selected_db = Database.objects.get(id=selected_db_id)

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

    # Rendu de la page avec les séquences immédiatement disponibles
    return render(request, 'blast_request.html', {
        'databases': databases,
        'sequences': sequences,
        'redirect_url': redirect_url,
        'error_message': error_message,
    })
