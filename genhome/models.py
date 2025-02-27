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
        related_name='owned_fa_sequences',
        null=True,  
        blank=True  # Allow to be empty
    )

    annotateur = models.ForeignKey(
        'authentication.BioinfoUser',
        on_delete=models.CASCADE,
        related_name='annotated_fa_sequences',
        null=True,  
        blank=True  # Allow to be empty
    )

    identifiant=models.CharField(
        max_length=100,
        default='Non defini'
    )
    genome = models.ForeignKey(
        'annotation.Genome', 
        on_delete=models.CASCADE, 
        related_name='sequence',
        default=1
    )
    def __str__(self):
        owner_str = ""
        if self.owner is not None:
            f"Owner: {self.owner.email},"
        return f"Statue :{self.status}, {owner_str} Sequence: {self.sequence[:30]}...,id: {self.id},"
