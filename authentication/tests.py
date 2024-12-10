from django.test import TestCase
from authentication.models import BioinfoUser

class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = BioinfoUser.objects.create_user(
            email="testuser@example.com",
            password="securepassword123"
        )
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("securepassword123"))

    def test_create_superuser(self):
        superuser = BioinfoUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword123"
        )
        self.assertTrue(superuser.is_admin)

    def test_user_list(self):
        BioinfoUser.objects.create_user(email="user1@example.com", password="password123")
        BioinfoUser.objects.create_user(email="user2@example.com", password="password456")

        users = BioinfoUser.objects.all()
        self.assertEqual(users.count(), 2)
