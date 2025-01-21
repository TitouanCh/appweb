from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from authentication.models import BioinfoUser
from django.http import HttpResponseForbidden
#source: https://www.codeswithpankaj.com/post/create-a-login-logout-system-in-django-step-by-step-instructions

def login_view(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'authentication/login.html', {'error': 'Erreur d\'authentification'})
    else:
        return render(request, 'authentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('/login')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        requested_role = request.POST['role']
        user = BioinfoUser.objects.create_user(email, password, requested_role=requested_role)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'authentication/signup.hmtl',
                          {'error': 'Echec de la création du compte'})
    else:
        return render(request, 'authentication/signup.html')

def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to view your profile.")

    return render(request, 'authentication/profile.html')
