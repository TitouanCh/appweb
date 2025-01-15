from django.http import HttpResponseForbidden
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import FaSequence
from django.urls import reverse
from annotation.forms import FaSequenceForm
from django.contrib import messages
from django.core.exceptions import ValidationError

def home(request):
    #homepage avec toute les sequences 
    sequences = FaSequence.objects.all()
    return render(request, 'genhome/index.html', {'sequences':sequences})
