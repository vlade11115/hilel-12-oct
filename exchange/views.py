from django.http import JsonResponse
from django.shortcuts import render

from .models import Rate


def main_view(request):
    response_data = {
        "current_rates": [
            {
                "id": rate.id,
                "date": rate.date,
                "vendor": rate.provider,
                "currency_a": rate.currency_from,
                "currency_b": rate.currency_to,
                "sell": rate.sell,
                "buy": rate.buy,
            }
            for rate in Rate.objects.all()
        ]
    }
    return JsonResponse(response_data)


def currency_exchange(request):
    best_rates = {}
    currencies = Rate.objects.values_list('currency_from', flat=True).distinct()
    for currency in currencies:
        best_rate = Rate.objects.filter(currency_from=currency).order_by('-sell').first()
        best_rates[currency] = best_rate

    context = {'best_rates': best_rates}
    return render(request, 'currency_exchange.html', context)


def exchange_result(request):
    if request.method == 'POST':
        from_currency = request.POST['from_currency']
        amount = float(request.POST['amount'])

        best_rate = Rate.objects.filter(currency_from=from_currency).order_by('-sell').first()

        if best_rate:
            result = amount * best_rate.sell
            return render(request, 'exchange_result.html', {'result': result, 'currency': from_currency})

    return render(request, 'error.html', {'message': 'Ошибка в расчете обмена валюты'})
