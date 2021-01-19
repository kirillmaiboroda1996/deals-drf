import csv
import io

from django.db.models import Sum

from .models import Deal


def _import_from_csv(dict_reader):
    """The function creates objects of Deal model from given DictReader obj."""
    for row in dict_reader:
        Deal.objects.create(**row)


def _get_csv_dict(serializer):
    csv_file = serializer.validated_data['file']

    decoded_file = csv_file.read().decode()
    io_string = io.StringIO(decoded_file)
    reader_from_csv = csv.DictReader(io_string)
    return reader_from_csv


def get_best_five_deals():
    deals = list(
        Deal.objects.values('customer')
            .annotate(total=Sum('total'))
            .order_by('total').reverse()[:5]
    )

    deals = [{'username': item['customer'], 'spent_money': item['total']} for item in deals]

    deals = [
        {
            'username': item['username'],
            'spent_money': item['spent_money'],
            'gems': list(set(Deal.objects.filter(customer=item['username']).values_list('item', flat=True)))
        }
        for item in deals
    ]
    return deals
