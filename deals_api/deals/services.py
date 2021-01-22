import csv
import io
import json

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response

from .models import Deal
from django_celery_results.models import TaskResult


def _get_common_gems(best_five_deals):
    """
    The function returns name of gems were bought
    by at least two of the top five list
    and this customer is one of these buyers

    """
    for deal in best_five_deals:
        deal_copy = best_five_deals.copy()
        deal_copy.pop(best_five_deals.index(deal))
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
    best_five_deals = list(
        Deal.objects.values('customer')
            .annotate(total=Sum('total'))
            .order_by('total').reverse()[:5]
    )

    best_five_deals = [{'username': item['customer'], 'spent_money': item['total']} for item in best_five_deals]

    best_five_deals = [
        {
            'username': item['username'],
            'spent_money': item['spent_money'],
            'gems': list(
                set(Deal.objects.filter(customer=item['username']).values_list('item', flat=True))
            )
        }
        for item in best_five_deals
    ]
    _get_common_gems(best_five_deals)

    return best_five_deals


def get_json_data_from_csv(serializer):
    """
    The function returns Json Data from csv file,
    for saving in db and celery tasks.

    """
    try:
        csv_file = serializer.validated_data['file']
        if not csv_file:
            return Response(
                {'Status': 'Error', 'Description': 'No data'},
                status=status.HTTP_400_BAD_REQUEST
            )

        decoded_file = csv_file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader_from_csv = csv.DictReader(io_string)
        json_data = [dict(i) for i in reader_from_csv]

        if not json_data:
            return Response(
                {'Status': 'Error', 'Description': 'Invalid encoding. UTF-8 is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except UnicodeDecodeError:
        return None

    return json_data


def get_task_result(task_id):
    """Function returns csv import result."""
    try:
        result = TaskResult.objects.get(task_id=task_id)
        result = json.loads(result.result)
    except ObjectDoesNotExist:
        result = {'status': 'Wrong id!'}
    return result
