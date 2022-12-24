from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from authentication.models import User
# Create your tests here.


class ModelTest(TestCase):

    def test_registeration(self):
        pass

    def test_user_creation(self):
        email = 'random@random.com'
        password = 'abcd123'
        create_user = get_user_model().objects.create(
            email=email,
        )
        create_user.set_password(password)
        create_user.save()
        self.assertEqual(create_user.email, email)
        self.assertTrue(create_user.check_password(password))

    def test_superuser_creation(self):
        email = 'random@random.com'
        password = 'abcd123'
        create_user = get_user_model().objects.create(
            email=email,
            is_superuser=True
        )
        create_user.set_password(password)
        create_user.save()
        self.assertEqual(create_user.email, email)
        self.assertEqual(create_user.is_superuser, True)
        self.assertTrue(create_user.check_password(password))


class RegisterationTest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('authtoken')
        return super().setUp()

    def test_register_returns_201(self):
        payload = {
            "email": "abc@gmail.com",
            "password": "random1234"
        }
        response = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registeration_duplicate_400(self):
        payload = {
            "email": "abc@gmail.com",
            "password": "random1234"
        }
        self.client.post(self.url, data=payload, format="json")
        response2 = self.client.post(self.url, data=payload, format="json")

        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class VerifyToken(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('verify')
        self.url_login = reverse('login')
        user = User.objects.create(email="moeedlodhi@gmail.com")
        user.set_password('ufc112233')
        user.save()
        payload = {
            "email": "abc@gmail.com",
            "password": "random1234"
        }
        user = User.objects.create(email=payload['email'])
        user.set_password(payload['password'])
        user.save()
        response = self.client.post(self.url_login, data=payload, format="json")
        self.jwt_token = response.data['data']['token']
        token = {'HTTP_AUTHORIZATION': 'Bearer ' + response.data['data']['token']}
        self.client.credentials(**token)
        return super().setUp()

    def test_verify_returns_200(self):
        response2 = self.client.post(self.url, data={"token": self.jwt_token})
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class LoginTest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('login')
        return super().setUp()

    def test_login_returns_200(self):
        payload = {
            "email": "abc@gmail.com",
            "password": "random1234"
        }
        user = User.objects.create(email=payload['email'])
        user.set_password(payload['password'])
        user.save()
        response2 = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_login_returns_400(self):
        payload = {
            "email": "abc@gmail.com",
            "password": "random1234"
        }
        user = User.objects.create(email=payload['email'])
        user.set_password('random')
        user.save()
        response2 = self.client.post(self.url, data=payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
