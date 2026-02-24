from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from order.serializers import OrderSerializer

class OrderViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all().order_by("id")