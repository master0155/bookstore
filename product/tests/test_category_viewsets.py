import json
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse

from product.factories import ProductFactory, CategoryFactory
from order.factories import OrderFactory, UserFactory
from product.models import Category


class TestCategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(
            title="books",
        )

    def test_get_all_categories(self):
        response = self.client.get(reverse("category-list", args=["v1"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)
        self.assertIn('results', category_data)
        self.assertIsInstance(category_data['results'], list)
        self.assertGreater(len(category_data['results']), 0)
        self.assertEqual(category_data['results'][0]["title"], self.category.title)

    def test_create_category(self):
        data = json.dumps(
            {
                "title": "technology",
            }
        )

        response = self.client.post(
            reverse("category-list", args=["v1"]),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title="technology")
        self.assertEqual(created_category.title, "technology")

