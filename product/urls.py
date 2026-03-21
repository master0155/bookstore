from django.urls import path, include, re_path
from rest_framework import routers

from product import viewsets

router = routers.SimpleRouter()
router.register(r'products', viewsets.ProductViewSet, basename='product')
router.register(r'categories', viewsets.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]