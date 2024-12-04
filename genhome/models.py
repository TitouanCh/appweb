from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=254, primary_key=True)
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=128)
    bio = models.CharField(max_length=1024)
    avatar = models.ImageField(upload_to='profile_images')
    status = models.TextChoices(
            "Guest", "User", "Admin"
    )

class FaSequence(models.Model):
    status = models.TextChoices(
            "Full Genome", "Coding DNA Sequence", "Peptide Sequence"
    )
    sequence = models.TextField()

