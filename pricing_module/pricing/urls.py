from django.urls import path
from .views import CalculatePriceView

urlpatterns = [
    path('calculatePrice/', CalculatePriceView.as_view()),  # Include the pricing app URLs
]