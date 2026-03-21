from django.db import models
from django.contrib.auth.models import User

from product.models import Product

class Order(models.Model):
    product = models.ManyToManyField('product.Product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)