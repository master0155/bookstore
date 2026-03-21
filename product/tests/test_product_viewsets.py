import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory
from product.models import Product

class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.product = ProductFactory(title='pro controller', price=200)
    
    def test_get_all_products(self):
        category = CategoryFactory(title='electronics')
        product = ProductFactory(title='laptop', price=1500, category=[category])
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = json.loads(response.content)
        self.assertIn('results', product_data)
        self.assertIsInstance(product_data['results'], list)
        self.assertGreater(len(product_data['results']), 0)
        first_product = product_data['results'][0]
        self.assertEqual(first_product['title'], product.title)
        self.assertEqual(float(first_product['price']), float(product.price))
        self.assertEqual(first_product['active'], product.active)
        self.assertEqual(first_product['category'][0]['title'], category.title)

    def test_create_product(self):
        category = CategoryFactory()
        data = json.dumps({
            'title': 'smartphone',
            'description': 'latest model',
            'price': 999.99,
            'categories_id': [category.id]
        })

        response = self.client.post(reverse('product-list'), data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_product = Product.objects.get(title='smartphone')

        self.assertEqual(created_product.description, 'latest model')
        self.assertEqual(float(created_product.price), 999.99)