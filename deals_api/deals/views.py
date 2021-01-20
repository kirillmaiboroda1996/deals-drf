from rest_framework import status, viewsets
from rest_framework.response import Response
import json
from .models import Deal
from .serializers import (
    FileUploadSerializer,
    DealListSerializer,
)
from .services import (
    get_json_data,
    get_best_five_deals
)

from .tasks import import_from_csv


class DealViewSet(viewsets.ModelViewSet):
    """list action - returns five deals by get_best_five_deals function.

    create action - saves data in db table Deals from requested csv file.
    get_serializer_class - returns serializers in depends witch request method was send.

    """
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

        reader_from_csv = get_json_data(serializer)
        import_from_csv.delay(reader_from_csv)

        return Response(status=status.HTTP_200_OK)
