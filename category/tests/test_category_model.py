from django.test import TestCase
from category.models import Category

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Exemplo")
        self.assertEqual(category.name, "Exemplo")