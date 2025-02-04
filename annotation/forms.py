from django import forms
from genhome.models import FaSequence

class FaSequenceForm(forms.ModelForm):
    class Meta:
        model = FaSequence
        fields = ['status','existing_genome', 'new_genome']  # Ajouter un champ pour le fichier
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        # Champ pour télécharger un fichier FASTA
    sequence_file = forms.FileField(label="Téléchargez votre fichier FASTA", required=True)
    existing_genome = forms.ModelChoiceField(
        queryset=Genome.objects.all(), 
        required=False, 
        empty_label="Sélectionner un génome existant"
    )
    new_genome = forms.CharField(
        max_length=100, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Ou entrez un nouveau génome'})
    )