from rest_framework import viewsets

from core.models import Ingredient
from core.permissions import ChatbotOrReadOnly
from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [ChatbotOrReadOnly]
