from django import forms
from .models import FaSequence

class FaSequenceForm(forms.ModelForm):
    class Meta:
        model = FaSequence
        fields = ['status']  # Ajouter un champ pour le fichier
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        # Champ pour télécharger un fichier FASTA
    sequence_file = forms.FileField(label="Ou téléchargez votre fichier FASTA", required=True)