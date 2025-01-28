from django.db import models


class Database(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    blastn_url = models.URLField(blank=True, null=True)  # URL pour BlastN
    blastp_url = models.URLField(blank=True, null=True)  # URL pour BlastP

    def __str__(self):
        return self.name

