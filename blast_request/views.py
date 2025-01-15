from django.shortcuts import render, redirect
from .models import Database


def database_list(request):
    databases = Database.objects.all()
    if request.method == "POST":
        selected_db_id = request.POST.get("database")
        selected_db = Database.objects.get(id=selected_db_id)
        return redirect(selected_db.url)
    return render(request, "blast_request.html", {"databases": databases})
