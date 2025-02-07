from django.db import models
from genhome.models import FaSequence
from django.utils.translation import gettext_lazy as _

class Status(models.TextChoices):
    ATTENTE = 'A', _('Attente')
    VALIDE = 'V', _('Validé')
    REFUSE = 'R', _('Refusé')

class Annotation(models.Model):
    sequence = models.ForeignKey(
        'genhome.FaSequence', 
        on_delete=models.CASCADE, 
        related_name='annotations'
    )
    content = models.TextField()  # Le texte de l'annotation
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    status = models.CharField( # Le status de l'annotation d'abord en attente puis valide ou refuse par un validateur
        max_length=24,
        choices=Status.choices,
        default=Status.ATTENTE
    )

    owner = models.ForeignKey(
        'authentication.BioinfoUser',
        on_delete=models.CASCADE,
        related_name='annotations',
        null=True,  
        blank=True  # Allow to be empty
    )

    def __str__(self):
        owner_str = ""
        if self.owner is not None:
            owner_str = f"Owner: {self.owner.email},"
        return f"Annotation for Sequence ID {self.sequence.id}, {owner_str} Status: {self.status}"
    
    def get_status_as_html(self) -> str:
        match self.status:
            case Status.VALIDE:
                return '<b style="color: green;">Validé</b>'
            case Status.REFUSE:
                return '<b style="color: red;">Refusé</b>'
            case _:
                return '<b style="color: gray;">Attente</b>'
    
    def accept(self):
        self.status = Status.VALIDE
        self.save()

    def deny(self):
        self.status = Status.REFUSE
        self.save()

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
        null=True,  
        blank=True  # Allow to be empty
    )

    def get_status_capitalize(self) -> str:
        return self.status.replace("_", " ").capitalize()
    
    def get_value_capitalize(self) -> str:
        return self.value.capitalize()


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
    def __str__(self):
        return self.name

