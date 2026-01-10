from django.test import TestCase
from django.contrib.auth.models import User

from order.models import Order
from product.models import Product


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="gabriel",
            password="123456"
        )

        self.product = Product.objects.create(
            title="Livro Teste",
            description="Descrição",
            price=50.00,
            active=True
        )

    def test_order_create(self):
        order = Order.objects.create(user=self.user)
        order.product.add(self.product)

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product.count(), 1)
