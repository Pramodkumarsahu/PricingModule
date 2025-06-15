from django.test import TestCase
from rest_framework.test import APIClient

from pricing.serializers import PriceInputSerializer
# Create your tests here.


class PriceCalculationTest(TestCase):
    def test_price_calculation(self):
        client = APIClient()
        data = {
            "total_km": 5,
            "total_minutes": 90,
            "waiting_minutes": 6
        }
        serializer = PriceInputSerializer(data=data)
        self.assertTrue(serializer.validate(data=data),"Serializer validation failed")
        response = client.post("pricing/calculatePrice/",data=data, format='json')
        self.assertEqual(response.status_code, 200)
