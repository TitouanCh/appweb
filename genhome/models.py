from django.db import models

#Faire class feature 
features_list=['chromosome','gene','transcript','gene_biotype','transcript_biotype','gene_symbol','description']

class FaSequence(models.Model):
    status = models.CharField(
        max_length=50,
        choices=[
            ("Full Genome", "Full Genome"),
            ("Coding DNA Sequence", "Coding DNA Sequence"),
            ("Peptide Sequence", "Peptide Sequence"),
        ],
        default="Coding DNA Sequence"  # 
    )
    sequence = models.TextField()
    owner = models.ForeignKey(
        'authentication.BioinfoUser',
        on_delete=models.CASCADE,
        related_name='fa_sequences',
        default=1 # TODO: changer
    )
    features_names=models.TextField( default=('|').join(features_list))
    features_val=models.TextField(default=('|').join(['non defini' for i in features_list]))
    def __str__(self):
        return f"Statue :{self.status}, Owner: {self.owner.email}, Sequence: {self.sequence[:30]}...,id: {self.id},"
