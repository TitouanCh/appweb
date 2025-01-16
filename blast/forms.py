from django import forms

class SequenceForm(forms.Form):
    sequence = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Enter your sequence here"}),
        label="Enter a custom sequence",
        required=True
    )
