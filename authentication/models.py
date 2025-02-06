from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from genhome.models import FaSequence
from annotation.models import Annotation

class BioinfoUserManager(BaseUserManager):
    def create_user(self, email, password=None, requested_role=None, role=None, last_name=None, name=None, numero=None):
        # Create user
        if not email or not password:
            raise ValueError("Les utilisateurs doivent obligatoirement posséder une adresse mail et un mot de passe.")
            
        if self.model.objects.filter(email=email).exists():
            raise ValueError("Un utilisateur avec cette adresse mail existe déjà.")
        
        if len(password) < 3: # Seulement 3 plus de facilité dans le débugage
            raise ValueError("Le mot de passe doit faire au moins 3 charactères de long.")
        
        user = self.model(    
            email=self.normalize_email(email),
            last_name=last_name,
            name=name,
            numero=numero
        )
        user.set_password(password)
        if not role:
            role = Role.ATTENTE
        user.role = role
        user.save(using=self._db)

        # Send request for user role if needed
        if role == Role.ATTENTE:
            if not requested_role:
                requested_role = Role.LECTEUR
            RoleRequest.objects.create_role_request(requested_role=requested_role, requester=user)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password, role=Role.ADMIN)
        user.save(using=self._db)
        return user


class Role(models.TextChoices):
    ATTENTE = 'AT', _('Attente')
    LECTEUR = 'LE', _('Lecteur')
    ANNOTATEUR = 'AN', _('Annotateur')
    VALIDATEUR = 'VA', _('Validateur')
    ADMIN = 'AD', _('Admin')


class BioinfoUser(AbstractBaseUser):
    email = models.EmailField(
            verbose_name="email address",
            unique=True,
            max_length=255
    )
    date_joined = models.DateField(verbose_name="date joined",
                                   auto_now_add=True)
    is_active = models.BooleanField(default=True)

    role = models.CharField(
        max_length=24,
        choices=Role.choices,
        default=Role.ADMIN # A changer apres migration
    )

    name = models.CharField(verbose_name="prénom", default="Non renseigné", max_length=32)
    last_name = models.CharField(verbose_name="nom", default="Non renseigné", max_length=32)
    numero = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")]
    )

    objects = BioinfoUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.role == Role.ADMIN
    
    def owns_sequence(self) -> bool:
        return FaSequence.objects.filter(owner=self).exists()
    
    def get_owned_sequences(self) -> models.QuerySet[FaSequence]:
        return FaSequence.objects.filter(owner=self)
    
    def get_owned_annotations(self) -> models.QuerySet[Annotation]:
        return Annotation.objects.filter(owner=self)


class RoleRequestManager(models.Manager):
    def create_role_request(self, requester, requested_role):
        if requested_role not in dict(Role.choices):
            raise ValidationError(f"Invalid role: {requested_role}")

        return self.create(requester=requester, requested_role=requested_role)


class RoleRequest(models.Model):
    requested_role = models.CharField(
        max_length=24,
        choices=Role.choices,
        default=Role.LECTEUR
    )

    requester = models.ForeignKey(
        'authentication.BioinfoUser',
        on_delete=models.CASCADE,
        related_name='requester',
    )

    status = models.CharField(
        max_length=1,
        choices=[
            ("A", "Accepté"),
            ("P", "Attente"),
            ("D", "Refusé"),
        ],
        default="P"
    )

    date_submitted = models.DateField(verbose_name="Date de soumission",
                                   auto_now_add=True)

    objects = RoleRequestManager()

    def __str__(self):
        return f"User {self.requester} (actuellement: {self.requester.get_role_display()}) veut le rôle: {self.get_requested_role_display()}"

    def accept(self):
        self.requester.role = self.requested_role
        self.status = "A"
        self.requester.save()
        self.save()

    def deny(self):
        self.status = "D"
        self.requester.save()
        self.save()
