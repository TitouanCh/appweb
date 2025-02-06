from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse

def about_view(request):
    """
    Vue pour la page 'À propos'.
    """
    try:
        get_template("about.html")  # Vérifie si Django trouve le template
        return render(request, "about.html")
    except:
        return HttpResponse("<h1>Erreur : Django ne trouve pas about.html</h1>")
