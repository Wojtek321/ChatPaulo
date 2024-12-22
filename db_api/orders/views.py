from rest_framework import viewsets

from core.models import  Order
from core.permissions import ChatbotOrReadOnly
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [ChatbotOrReadOnly]
