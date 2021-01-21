from django.urls import path
from .views import DealViewSet, TaskResult

urlpatterns = [
    path('deals/', DealViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('get-request-status/<str:task_id>/', TaskResult.as_view())
]
