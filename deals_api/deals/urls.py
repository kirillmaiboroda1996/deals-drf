from django.urls import path
from .views import DealViewSet

urlpatterns = [
    path('uploads/', DealViewSet.as_view({'post': 'create', 'get': 'list'}))
]
