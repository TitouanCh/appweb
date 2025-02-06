from django import forms

class SequenceSearchForm(forms.Form):
    sequence = forms.CharField(
        max_length=500, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter sequence (optional)'})
    )
    species = forms.CharField(
        max_length=255, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter species (optional)'})
    )
