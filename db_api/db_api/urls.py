from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include('items.urls')),
    path('api/', include('ingredients.urls')),
    path('api/', include('orders.urls')),
]