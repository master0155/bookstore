from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal

from product.models.product import Product
from order.models.order import Order
from order.serializers.order_serializer import OrderSerializer


class OrderSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="gabriel", password="123456")

        self.p1 = Product.objects.create(
            title="P1",
            description="d1",
            price=Decimal("10.00"),
            active=True,
        )
        self.p2 = Product.objects.create(
            title="P2",
            description="d2",
            price=Decimal("15.50"),
            active=True,
        )

    def test_serialized_fields_and_total(self):
        order = Order.objects.create(user=self.user)
        order.product.add(self.p1, self.p2)

        data = OrderSerializer(order).data

        self.assertIn("product", data)
        self.assertIn("total", data)
        self.assertIn("user", data)
        # products_id is write-only
        self.assertNotIn("products_id", data)

        expected_total = float(self.p1.price + self.p2.price)
        # serializer returns numeric value; compare as float
        self.assertAlmostEqual(float(data["total"]), expected_total)

    def test_create_with_products_id(self):
        payload = {"products_id": [self.p1.id, self.p2.id], "user": self.user.id}
        serializer = OrderSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product.count(), 2)
