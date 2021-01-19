from django.urls import path, include
from rest_framework import routers

from .views import DealViewSet

router = routers.SimpleRouter()
router.register(r'allmethods', DealViewSet, basename='allmethods')

urlpatterns = [
]
urlpatterns += router.urls