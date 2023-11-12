from django.urls import path
from .views import currency_exchange, exchange_result

urlpatterns = [
    path('currency_exchange/', currency_exchange, name='currency_exchange'),
    path('exchange_result/', exchange_result, name='exchange_result'),
]
