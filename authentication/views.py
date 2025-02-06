from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from authentication.models import BioinfoUser, Role, RoleRequest
from django.http import HttpResponseForbidden, JsonResponse
import json
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
        last_name = request.POST['last_name']
        name = request.POST['name']
        numero = request.POST['numero']
        user = BioinfoUser.objects.create_user(email, password, requested_role=requested_role, last_name=last_name, name=name, numero=numero)
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
