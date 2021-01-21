from rest_framework import status, viewsets
from rest_framework.response import Response
import json

from rest_framework.views import APIView

from . import services
from .models import Deal
from .serializers import (
    FileUploadSerializer,
    DealListSerializer,
)
from .services import (
    get_json_data_from_csv,
    get_best_five_deals
)

from .tasks import import_from_csv


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return DealListSerializer
        if self.action == 'create':
            return FileUploadSerializer
        return DealListSerializer

    def list(self, request, *args, **kwargs):
        deals = get_best_five_deals()
        return Response(deals)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        json_data = get_json_data_from_csv(serializer)
        import_from_csv.delay(json_data)

        return Response(status=status.HTTP_200_OK)


class TaskResult(APIView):
    """Get the result of processing a request."""
    def get(self, request, task_id):
        result = services.get_task_result(task_id)
        return Response(result)
