from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from authentication.models import BioinfoUser, Role, RoleRequest
from django.http import HttpResponseForbidden, JsonResponse
import json
#source: https://www.codeswithpankaj.com/post/create-a-login-logout-system-in-django-step-by-step-instructions


def login_view(request):
    # Si l'utilisateur est déjà connecté, le rediriger vers la page demandée ou l'accueil
    if request.user.is_authenticated:
        return redirect(request.session.pop('next', '/'))

    # Si l'utilisateur arrive sur la page login avec une URL 'next', on la stocke en session
    if 'next' in request.GET:
        request.session['next'] = request.GET['next']

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.session.pop('next', '/')  # Récupère l'URL stockée ou redirige vers "/"
            return redirect(next_url)  # Redirection après connexion
    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        requested_role = request.POST.get('role')
        last_name = request.POST.get('last_name')
        name = request.POST.get('name')
        numero = request.POST.get('numero')
        try:
            user = BioinfoUser.objects.create_user(email, password, requested_role=requested_role, last_name=last_name, name=name, numero=numero)
        except ValueError as e:
            return render(request, 'authentication/signup.html', {'error': f'Echec de la création du compte : {e}'})

        if user is not None:
            login(request, user)
            msg = "Création de compte réussie, attendez la validation de votre rôle par un admin."
            return redirect(f'/?message={msg}')
        else:
            return render(request, 'authentication/signup.html',
                          {'error': 'Echec de la création du compte'})
    else:
        return render(request, 'authentication/signup.html')

def profile_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to view your profile.")
    
    owned_annotation = request.user.get_owned_annotations()
    owned_sequences = request.user.get_owned_sequences()

    return render(request, 'authentication/profile.html', {"annotations": owned_annotation, "sequences": owned_sequences})

def request_view(request):
    if not(request.user.is_staff):
        return HttpResponseForbidden("You need to be an admin to view this page.")
    
    requests = RoleRequest.objects.all()
    return render(request, 'authentication/role-request.html', {'requests': requests})

def process_request(request):
    if not(request.user.is_staff):
        return HttpResponseForbidden("You need to be an admin to view this page.")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data
            request_id = data.get('request_id', None)
            action_type = data.get('type', None)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        req = RoleRequest.objects.get(id=request_id)
        if action_type == "accept":
            req.accept()
            return JsonResponse({'request_id': request_id, 'type': action_type, 'display': 'Acceptée'})
        elif action_type == "deny":
            req.deny()
            return JsonResponse({'request_id': request_id, 'type': action_type, 'display': 'Refusée'})

        return JsonResponse({'error': 'Invalid type'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
