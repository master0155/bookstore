import json

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from django.urls import reverse

from product.factories import ProductFactory, CategoryFactory
from order.factories import OrderFactory, UserFactory
from product.models import Product
from order.models import Order

class OrderViewSetTest(APITestCase):

    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.catergory = CategoryFactory(title='technology')
        self.product = ProductFactory(title='mouse', price=100, category=[self.catergory])
        self.order = OrderFactory(Product=[self.product], user=self.user)

    def test_order(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertIn('results', order_data)
        self.assertIsInstance(order_data['results'], list)
        self.assertGreater(len(order_data['results']), 0)
        first_order = order_data['results'][0]
        self.assertEqual(first_order['product'][0]['title'], self.product.title)
        self.assertEqual(first_order['product'][0]['price'], self.product.price)
        self.assertEqual(first_order['product'][0]['active'], self.product.active)
        self.assertEqual(first_order['product'][0]['category'][0]['title'], self.catergory.title)

    def test_create_order(self):
        user = UserFactory()
        product2 = ProductFactory(title='keyboard', price=150, category=[self.catergory])
        payload = {
            'products_id': [self.product.id, product2.id],
            'user': user.id
        }
        response = self.client.post(reverse('order-list'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)