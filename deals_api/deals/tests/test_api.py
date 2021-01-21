from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from deals.models import Deal


class DealsApiTestCase(APITestCase):
    def test_get(self):
        deal1 = Deal.objects.create(
            customer='test_customer1',
            item='тест',
            total=1000,
            quantity=5,
            date='2018-12-14 08:29:52.506166'
        )

        deal2 = Deal.objects.create(
            customer='test_customer2',
            item='тест',
            total=1000,
            quantity=5,
            date='2018-12-14 08:29:52.506166'
        )
        url = reverse('deals-list')
        response = self.client.get(url)
        data = [{'username': 'test_customer1', 'spent_money': 1000, 'gems': ['тест']},
                {'username': 'test_customer2', 'spent_money': 1000, 'gems': ['тест']}]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data, response.data)
