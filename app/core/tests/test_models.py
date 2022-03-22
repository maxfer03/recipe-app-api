from unicodedata import name
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch

def sample_user(email="test@test.com", password="test123pass"):
  """Creating a sample user"""

  return get_user_model().object.create_user(email, password)


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

    def test_create_new_superuser(self):
        """Test creating a new Superuser"""
        user = get_user_model().object.create_superuser(
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
      """Test tag string representation"""
      tag = models.Tag.objects.create(
        user=sample_user(),
        name="Vegan"
      )
      self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
      """Test the ingredient string representation"""
      ingredient = models.Ingredient.objects.create(
        user=sample_user(),
        name='Cucumber'
      )

      self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
      """Test the recipe string representation"""
      recipe = models.Recipe.objects.create(
        user=sample_user(),
        title='Steak and mushroom sauce',
        time_minutes= 5,
        price= 5.00
      )

      self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that img is saved in the correct location"""
        uuid = 'test-uuid'

        mock_uuid.return_value = uuid

        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)