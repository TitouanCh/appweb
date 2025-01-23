from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models

class BioinfoUserManager(BaseUserManager):
    def create_user(self, email, password=None, requested_role=None, role=None):
        # Create user
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
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
