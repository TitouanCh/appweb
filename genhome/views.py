from django.http import HttpResponseForbidden
from django.template import loader
from django.shortcuts import render, get_object_or_404,redirect
from .models import FaSequence
from django.urls import reverse
from annotation.forms import FaSequenceForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from annotation.models import Genome

def home(request):
    #homepage avec toute les genomes
    genomes = Genome.objects.all()
    return render(request, 'genhome/index.html', {'genomes':genomes})
