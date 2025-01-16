from django import forms

class SequenceSearchForm(forms.Form):
    sequence = forms.CharField(max_length=255, required=False, help_text="Enter a nucleotide/protein sequence (min 3 characters).")
    species = forms.CharField(max_length=255, required=False, help_text="Enter species name.")
    output_type = forms.ChoiceField(choices=[('genome', 'Genome'), ('gene_protein', 'Gene/Protein')], required=True)
