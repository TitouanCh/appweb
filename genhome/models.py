from django.db import models

class FaSequence(models.Model):
    #status = models.TextChoices(
    #        "Full Genome", "Coding DNA Sequence", "Peptide Sequence"
    #)
    sequence = models.TextField()


class Annotation(models.Model):
    sequence = models.ForeignKey(FaSequence, on_delete=models.CASCADE, related_name="annotations")