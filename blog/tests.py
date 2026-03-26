from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

class AuthAndPostTests(TestCase):

    def setUp(self):
        # Створюємо звичайного користувача
        self.user = User.objects.create_user(
            username='testuser', password='123456', email='user@example.com'
        )
        # Створюємо адміна
        self.admin = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@example.com'
        )

        # APIClient для DRF
        self.client = APIClient()

    def test_login_user(self):
        # Перевірка входу користувача
        response = self.client.post('/api/login/', {
            'username': 'testuser',
            'password': '123456'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_post_as_user(self):
        # Звичайний користувач пробує створити пост
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {
            "title": "Test Post",
            "content": "This is a test.",
            "author": self.user.id,
            "category": "Testing"
        }
        response = self.client.post('/api/posts/', data, format='json')
        # Звичайний користувач не повинен мати права на створення посту
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_post_as_admin(self):
        # Адмін створює пост
        token = Token.objects.create(user=self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        data = {
            "title": "Admin Post",
            "content": "Created by admin.",
            "author": self.admin.id,
            "category": "Admin"
        }
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_unique_email(self):
        # Перевірка реєстрації користувача з унікальним email
        data = {
            "username": "newuser",
            "password": "pass1234",
            "email": "user@example.com"  # email, що вже існує
        }
        response = self.client.post('/api/register/', data, format='json')
        # Має спрацювати валідація у серіалайзері
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_success(self):
        # Перевірка успішної реєстрації
        data = {
            "username": "uniqueuser",
            "password": "pass1234",
            "email": "unique@example.com"
        }
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)