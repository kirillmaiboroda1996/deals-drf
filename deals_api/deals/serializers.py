from rest_framework import serializers

from .models import Deal


class FileUploadSerializer(serializers.Serializer):
    """Serializer for form for csv uploads."""
    file = serializers.FileField()

    class Meta:
        fields = ('file',)


class DealListSerializer(serializers.Serializer):
    """Serializer for showing list of deals."""
    customer = serializers.CharField(max_length=250)
    item = serializers.CharField(max_length=250)
    total = serializers.CharField(max_length=250)
    quantity = serializers.IntegerField()
    date = serializers.DateTimeField()
