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
    identifiant=models.CharField(
        max_length=100,
        default='Non defini'
    )
    genome = models.ForeignKey(
        'annotation.Genome', 
        on_delete=models.CASCADE, 
        related_name='Genome',
        default='non defini'
    )
    def __str__(self):
        return f"Statue :{self.status}, Owner: {self.owner.email}, Sequence: {self.sequence[:30]}...,id: {self.id},"
