from django.db import models

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
    def __str__(self):
        return f"Statue :{self.status}, Owner: {self.owner.email}, Sequence: {self.sequence[:30]}...,id: {self.id},"


class Annotation(models.Model):
    sequence = models.ForeignKey(
        'FaSequence', 
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

