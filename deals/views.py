from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from .serializers import (
    FileUploadSerializer,
    DealListSerializer
)
from .services import _import_from_csv, _get_csv_dict, get_best_five_deals
from .models import Deal


# class FileUploadAPIView(generics.CreateAPIView):
#     serializer_class = FileUploadSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         csv_file = serializer.validated_data['file']
#
#         decoded_file = csv_file.read().decode()
#         io_string = io.StringIO(decoded_file)
#         reader_from_csv = csv.DictReader(io_string)
#
#         _import_from_csv(reader_from_csv)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class DealListView(generics.ListAPIView):
#     serializer_class = DealListSerializer
#     model = Deal
#
#     def get_queryset(self):
#         deals = Deal.objects.all()
#         return deals


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.filter(quantity=1)

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

        reader_from_csv = _get_csv_dict()
        _import_from_csv(reader_from_csv)
        return Response(status=status.HTTP_204_NO_CONTENT)
