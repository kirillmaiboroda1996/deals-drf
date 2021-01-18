import csv
import io

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import FileUploadSerializer
import json
from types import SimpleNamespace


def upload_delay(iter_obj):
    for row in iter_obj:
        row = json.dumps(row, indent=4, ensure_ascii=False)
        json_delay = json.loads(row, object_hook=lambda d: SimpleNamespace(**d))
        print(json_delay.customer, json_delay.item)


class FileUploadAPIView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        csv_file = serializer.validated_data['file']
        decoded_file = csv_file.read().decode()
        io_string = io.StringIO(decoded_file)
        dict_reader_from_csv = csv.DictReader(io_string)

        upload_delay(dict_reader_from_csv)
        return Response(status=status.HTTP_204_NO_CONTENT)
