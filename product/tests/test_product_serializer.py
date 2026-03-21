from django.test import TestCase
from decimal import Decimal

from product.models.category import Category
from product.models.product import Product
from product.serializers.product_serializer import ProductSerializer


class ProductSerializerTest(TestCase):

    def setUp(self):
        self.cat = Category.objects.create(
            title="Categoria",
            slug="categoria",
            description="desc",
            active=True,
        )

    def test_serialized_fields(self):
        product = Product.objects.create(
            title="Produto",
            price=Decimal("12.50"),
            active=True,
        )
        product.category.add(self.cat)

        data = ProductSerializer(product).data

        self.assertIn("id", data)
        self.assertIn("title", data)
        self.assertIn("description", data)
        self.assertIn("price", data)
        self.assertIn("active", data)
        self.assertIn("category", data)
        # write-only field must not appear in serialized output
        self.assertNotIn("categories_id", data)

    def test_create_with_categories_id(self):
        payload = {
            "title": "Novo",
            "price": "9.99",
            "active": True,
            "categories_id": [self.cat.id],
        }

        serializer = ProductSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()

        self.assertEqual(product.title, "Novo")
        self.assertEqual(product.category.count(), 1)
        self.assertIn(self.cat, product.category.all())
