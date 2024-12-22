from rest_framework import viewsets

from core.models import Item
from core.permissions import ChatbotOrReadOnly
from .serializers import ItemSerializer, MenuItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    permission_classes = [ChatbotOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return MenuItemSerializer
        return ItemSerializer