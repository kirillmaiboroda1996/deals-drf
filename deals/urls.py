from django.urls import path
from .views import FileUploadAPIView
urlpatterns = [
    path('v1/uploads', FileUploadAPIView.as_view(), name='upload')
]
