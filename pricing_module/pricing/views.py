from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import PricingConfig
from .serializers import PriceInputSerializer
# Create your views here.

from django.utils.timezone import now

class CalculatePriceView(APIView):
    def post(self, request):
        data = request.data
        serializer = PriceInputSerializer(data=data)
        if not serializer.validate(data):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        day = datetime.today().strftime('%a')  # E.g., 'Mon'
        config = PricingConfig.objects.filter(active=True).first()
        if config:
            # Check if the current day is applicable for the active pricing config
            if day not in config.days_applicable:
                return Response({"error": "Today's pricing config is not applicable."}, status=404)
        if not config:
            return Response({"error": "No active pricing config for today."}, status=404)

        total_km = data.get("total_km")
        total_minutes = data.get("total_minutes")
        waiting_minutes = data.get("waiting_minutes")

        # Distance Pricing
        if total_km <= config.distance_base_km:
            distance_cost = config.distance_base_price # Assuming distance_base_price is a flat rate for up to distance_base_km
        else:
            extra_km = total_km - config.distance_base_km
            distance_cost = config.distance_base_price + (extra_km * config.distance_additional_price) # Assuming distance_additional_price is per km

        # Time Multiplier
        time_cost = 0
        for multiplier in config.time_multipliers.all():
            if multiplier.from_minute <= total_minutes <= multiplier.to_minute:
                time_cost = total_minutes * multiplier.multiplier
                break

        # Waiting Charge
        wc = 0
        extra_waiting = max(waiting_minutes - config.free_waiting_minutes, 0)
        wc = (extra_waiting / 3) * config.waiting_charge
        price = distance_cost + time_cost + wc
        return Response({"total_price": round(price, 2)})
