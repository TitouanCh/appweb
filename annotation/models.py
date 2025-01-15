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
