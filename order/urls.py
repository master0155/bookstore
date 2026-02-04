from django.urls import path, include
from rest_framework.routers import routers
from order import viewsets

router = routers.register(r'orders', viewsets.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]