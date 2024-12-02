from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]