from django import forms
from .models import FaSequence

class FaSequenceForm(forms.ModelForm):
    class Meta:
        model = FaSequence
        fields = ['sequence','status']  #Champs obligatoire a sauvegarder 
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'sequence': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
