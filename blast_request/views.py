from django.shortcuts import redirect, render
from .models import Database

def database_list(request):
    databases = Database.objects.all()
    if request.method == "POST":
        return redirect('blast_request')
    return render(request, "blast_request.html", {"databases": databases})


def blast_request_view(request):
    """
    Vue pour gérer l'accès aux bases de données et rediriger vers BlastN ou BlastP
    avec la séquence préremplie selon le type.
    """
    databases = Database.objects.all()
    redirect_url = None
    error_message = None

    if request.method == 'POST':
        # Récupération des données du formulaire
        selected_db_id = request.POST.get('database')  # ID de la base sélectionnée
        sequence = request.POST.get('sequence', '').strip()  # Séquence saisie

        # Debug : Afficher la séquence et l'ID sélectionné
        print(f"Séquence saisie : {sequence}")
        print(f"ID de la base sélectionnée : {selected_db_id}")

        # Validation du champ séquence
        if all(base in "ATCGUatcgu" for base in sequence):  # Séquence nucléotidique
            tool = "blastn"
        elif all(aa in "ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy" for aa in sequence):  # Séquence peptidique
            tool = "blastp"
        else:
            error_message = "La séquence entrée est invalide. Veuillez vérifier votre saisie."
            print(f"Erreur de validation de séquence : {error_message}")  # Debug : Erreur
            return render(request, 'blast_request.html', {
                'databases': databases,
                'error_message': error_message
            })

        # Récupération de la base de données sélectionnée
        try:
            selected_db = Database.objects.get(id=selected_db_id)

            # Debug : Afficher les détails de la base sélectionnée
            print(f"Base sélectionnée : {selected_db.name}")
            print(f"URL générale : {selected_db.url}")
            print(f"BlastN URL : {selected_db.blastn_url}")
            print(f"BlastP URL : {selected_db.blastp_url}")

            # Utiliser l'URL appropriée en fonction du type de séquence
            if tool == "blastn" and selected_db.blastn_url:
                redirect_url = f"{selected_db.blastn_url}{sequence}"
                print(f"Redirection vers BlastN : {redirect_url}")  # Debug : URL générée pour BlastN
            elif tool == "blastp" and selected_db.blastp_url:
                redirect_url = f"{selected_db.blastp_url}{sequence}"
                print(f"Redirection vers BlastP : {redirect_url}")  # Debug : URL générée pour BlastP
            else:
                error_message = "La base de données sélectionnée ne supporte pas ce type de séquence."
                print(f"Erreur de compatibilité : {error_message}")  # Debug : Erreur

        except Database.DoesNotExist:
            error_message = "Base de données sélectionnée non valide."
            print(f"Erreur : {error_message}")  # Debug : Erreur

    # Debug : Afficher l'URL finale ou le message d'erreur
    print(f"URL utilisée pour la redirection : {redirect_url}")
    print(f"Message d'erreur : {error_message}" if error_message else "Aucune erreur détectée.")

    # Rendu de la page avec les bases disponibles et les erreurs ou redirections
    return render(request, 'blast_request.html', {
        'databases': databases,
        'redirect_url': redirect_url,
        'error_message': error_message
    })
