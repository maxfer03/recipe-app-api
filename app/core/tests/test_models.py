from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):

    
        """Test creating a new user with an email successfully"""
        email = "test@testmail.com"
        pw = "12345"
        user = get_user_model().object.create_user(
            email=email,
            password=pw
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(pw))

    def test_new_user_email_normalized(self):
        """Test The email for a new user is normalized"""
        email = "test@THISMAIL.COM"
        user = get_user_model().object.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating User with no email raises error"""
        email = None
        with self.assertRaises(ValueError):
            get_user_model().object.create_user(email, 'test123')

