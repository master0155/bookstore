import factory

from django.contrib.auth.models import User
from product.factories import ProductFactory
from order.models import Order

class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")

    class Meta:
        model = User

class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.LazyAttribute(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.product.add(product)
        else:
            self.product.add(ProductFactory())

    class Meta:
        model = Order