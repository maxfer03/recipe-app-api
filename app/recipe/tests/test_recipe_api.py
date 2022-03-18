from random import sample
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """Create and return sample recipe"""
    defaults = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """Test the publicly available Recipe API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that auth is required for retrieving Recipe"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateRecipeApiTests(TestCase):
    """Test the private Recipe API"""

    def setUp(self):
        self.user = get_user_model().object.create_user(
            'test@test.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipe_list(self):
        """Test retrieving a list of recipes"""
        recipe_1 = sample_recipe(
            self.user, title='Mondongo', time_minutes=5, price=2.00)
        recipe_2 = sample_recipe(self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test that only recipes for the auth user are returned"""
        user2 = get_user_model().object.create_user(
            'other@test.com',
            'testpass'
        )
        user2_recipe = sample_recipe(user=user2)
        user_recipe = sample_recipe(user=self.user, title="User's recipe")

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
