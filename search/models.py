from django.db import models
# Classses mortes à enlevées


class Genome(models.Model):
    name = models.CharField(max_length=255)
    sequence = models.TextField()
    species = models.CharField(max_length=255)


class GeneProtein(models.Model):
    name = models.CharField(max_length=255)
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE, related_name="genes_proteins")
    description = models.TextField()
    sequence = models.TextField()
