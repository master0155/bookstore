from django.test import TestCase
from product.models.product import Product


class ProductModelTest(TestCase):

    def test_product_create(self):
        product = Product.objects.create(
            title="Produto teste",
            price=10.50,
            active=True
        )

        self.assertEqual(product.title, "Produto teste")
        self.assertEqual(product.price, 10.50)
