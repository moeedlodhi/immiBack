from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.


class ModelTest(TestCase):

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
