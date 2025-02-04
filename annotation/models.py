from django.db import models
from genhome.models import FaSequence

class Annotation(models.Model):
    sequence = models.ForeignKey(
        'genhome.FaSequence', 
        on_delete=models.CASCADE, 
        related_name='annotations'
    )
    content = models.TextField()  # Le texte de l'annotation
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    owner = models.ForeignKey(
        'authentication.BioinfoUser',
        on_delete=models.CASCADE,
        related_name='annotations',
        default=1 # TODO: changer
    )
    def __str__(self):
        return f"Annotation for Sequence ID {self.sequence.id}, Owner: {self.owner.email}"

#Faire class feature 
features_list=['chromosome','gene','transcript','gene_biotype','transcript_biotype','gene_symbol','description']

class Feature(models.Model):
    status = models.CharField(
        max_length=100,
        choices=[
            ("chromosome", "chromosome"),
            ("gene", "gene"),
            ("transcript", "transcript"),
            ("gene_biotype", "gene_biotype"),
            ("transcript_biotype", "ranscript_biotype"),
            ("gene_symbol", "gene_symbol"),
        ],
    )
    value=models.TextField(default='non defini')
    sequence = models.ForeignKey(
        'genhome.FaSequence', 
        on_delete=models.CASCADE, 
        related_name='feature'
    )
    owner = models.ForeignKey(
        'authentication.BioinfoUser',
        on_delete=models.CASCADE,
        related_name='feature',
        default=1 # TODO: changer
    )


class Genome(models.Model) : 
    name=models.CharField(
        max_length=100,
        default='non defini'
    )
    annotation_state=models.CharField(
        max_length=100,
        choices=[
            ("in_progress", "in progress"),
            ("fully", "fully"),
        ],
        default='in_progress'
    ) # A changer par le validateur 

