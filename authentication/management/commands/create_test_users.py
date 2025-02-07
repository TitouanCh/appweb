from django.core.management.base import BaseCommand
from authentication.models import BioinfoUser, Role
from annotation.views import import_sequences
import random

class Command(BaseCommand):
    help = 'Créé des utilisateurs test avec différents rôles (5 annotateurs, 4 validateurs, 1 admin). Tout les utilisateurs ont le même mot de passe.'

    def handle(self, *args, **kwargs):
        def generate_french_phone_number() -> str:
            phone_number = "06"
            for _ in range(4):
                phone_number += f" {random.randint(0, 99):02d}"
            return phone_number
        
        users = [
            # Annotateurs ===
            {
                "name": "Guy-Manuel",
                "role": Role.ANNOTATEUR,
                "last_name": "Homem-Christo",
                "email": "guy@gmail.com",
                "numero": generate_french_phone_number(),
            },
            {
                "name": "Thomas",
                "role": Role.ANNOTATEUR,
                "last_name": "Bangalter",
                "email": "thomas@gmail.com",
                "numero": generate_french_phone_number(),
            },
            {
                "name": "Nicolas",
                "role": Role.ANNOTATEUR,
                "last_name": "Jaar",
                "email": "nicolas@gmail.com",
                "numero": generate_french_phone_number(),
            },
            {
                "name": "Joachim",
                "role": Role.ANNOTATEUR,
                "last_name": "Pastor",
                "email": "joe@gmail.com",
                "numero": generate_french_phone_number(),
            },
            {
                "name": "Simon",
                "role": Role.ANNOTATEUR,
                "last_name": "Henner",
                "email": "simon@gmail.com",
                "numero": generate_french_phone_number(),
            },

            # Validateur ===
            {
                "name": "Kid",
                "role": Role.VALIDATEUR,
                "last_name": "Francescoli",
                "email": "kid@gmail.com",
                "numero": generate_french_phone_number(),
            },
            {
                "name": "Joris",
                "role": Role.VALIDATEUR,
                "last_name": "Delacroix",
                "email": "delacroix@gmail.com",
                "numero": generate_french_phone_number(),
            },
            {
                "name": "Joris",
                "role": Role.VALIDATEUR,
                "last_name": "Voorn",
                "email": "joris@gmail.com",
                "numero": generate_french_phone_number(),
            },
            {
                "name": "Kevin",
                "role": Role.VALIDATEUR,
                "last_name": "Rodrigues",
                "email": "kevin@gmail.com",
                "numero": generate_french_phone_number(),
            },

            # Admin ===
            {
                "name": "Pascal",
                "role": Role.ADMIN,
                "last_name": "Arbez-Nicolas",
                "email": "admin@gmail.com",
                "numero": generate_french_phone_number(),
            },
        ]
        
        same_password = '123'

        for user in users:
            self.stdout.write(self.style.NOTICE(f"Création de l'utilisateur : {user['email']}"))
            try:
                new_user = BioinfoUser.objects.create_user(user["email"], same_password, role=user["role"], last_name=user["last_name"], name=user["name"], numero=user["numero"])
                self.stdout.write(self.style.SUCCESS(f"Utilisateur créé avec succès : {new_user}, role : {new_user.get_role_display()}"))
            except ValueError as e:
                self.stdout.write(self.style.WARNING(f"Echec de la création de l'utilisateur : {e}"))

    # Command to delete all users: BioinfoUser.objects.all().delete()