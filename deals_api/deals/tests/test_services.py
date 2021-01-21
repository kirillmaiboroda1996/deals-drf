from django.test import TestCase
from deals.services import (
    get_best_five_deals,
    _get_common_gems,
)

from deals.models import Deal


class ServiceTestCase(TestCase):
    def test_best_five_deals(self):
        deal1 = Deal.objects.create(
            customer='test_customer1', item='тест1', quantity=5, total=1500,
            date='2018-12-14 08:29:52.506166'
        )

        deal2 = Deal.objects.create(
            customer='test_customer2', item='тест2', quantity=5, total=1100,
            date='2018-12-14 08:29:52.506166'
        )

        deal3 = Deal.objects.create(
            customer='test_customer3', item='тест3', quantity=5, total=1200,
            date='2018-12-14 08:29:52.506166'
        )

        deal4 = Deal.objects.create(
            customer='test_customer1', item='тест2', quantity=5, total=1100,
            date='2018-12-14 08:29:52.506166'
        )

        deal5 = Deal.objects.create(
            customer='test_customer2', item='тест1', quantity=5, total=1500,
            date='2018-12-14 08:29:52.506166'
        )

        data = [{'username': 'test_customer1', 'spent_money': 2600, 'gems': ['тест1', 'тест2']},
                {'username': 'test_customer2', 'spent_money': 2600, 'gems': ['тест1', 'тест2']},
                {'username': 'test_customer3', 'spent_money': 1200, 'gems': []}]

        result = get_best_five_deals()

        self.assertEqual(data, result)
