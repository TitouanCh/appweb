from django.db import models

class FaSequence(models.Model):
    status = models.TextChoices(
            "Full Genome", "Coding DNA Sequence", "Peptide Sequence"
    )
    sequence = models.TextField()


class Annotation(models.Model):
    sequence = models.ForeignKey(
        'FaSequence', 
        on_delete=models.CASCADE, 
        related_name='annotations'
    )
    content = models.TextField()  # Le texte de l'annotation
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f"Annotation for Sequence ID {self.sequence.id}"

