from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as doc_urls

from deals.views import DealViewSet, TaskResult


router = DefaultRouter()
router.register(r'deals', DealViewSet, basename='deals')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('get-request-status/<str:task_id>/', TaskResult.as_view()),

]
urlpatterns += doc_urls
