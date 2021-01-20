import csv
import io

from django.db.models import Sum

from .models import Deal


def _get_common_gems(deals):
    """The function returns gems witch was buying 2 or more customers."""
    for deal in deals:
        deal_copy = deals.copy()
        deal_copy.pop(deals.index(deal))
        current_deal_crossing_gems = []
        for deal_copy in deal_copy:
            crossing_gems = list(set(deal['gems']) & set(deal_copy['gems']))
            if crossing_gems:
                current_deal_crossing_gems.extend(crossing_gems)
        deal['gems'] = current_deal_crossing_gems


def get_best_five_deals():
    """
    The function returns best five deals by customer.

    And returns gems of customer if gems was buying also other customer
    in top 5 deals from _get_common_gems func.

    """
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
            'gems': list(
                set(
                    Deal.objects.filter(customer=item['username'])
                        .values_list('item', flat=True)
                )
            )
        }
        for item in deals
    ]

    _get_common_gems(deals)
    return deals


def import_from_csv(dict_reader):
    """The function creates objects of Deal model from given DictReader obj."""
    for row in dict_reader:
        Deal.objects.create(**row)


def get_csv_dict(serializer):
    """The function returns DictReader object."""
    csv_file = serializer.validated_data['file']

    decoded_file = csv_file.read().decode()
    io_string = io.StringIO(decoded_file)
    reader_from_csv = csv.DictReader(io_string)
    return reader_from_csv
