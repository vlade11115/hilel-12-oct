from django.urls import path
from .views import exchange_rates, currency_exchange_calculator

urlpatterns = [
    path("", currency_exchange_calculator, name="currency_exchange_calculator"),
    path("exchange_rates", exchange_rates, name="exchange_rates"),
]
