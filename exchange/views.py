from django.http import JsonResponse
from django.shortcuts import render

from .forms import CalculatorForm
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


def calculator(request):
    #  Використовувати валюти з БД, з кращим курсом для користувача.

    if request.method == 'GET':
        form = CalculatorForm()
        data = {'form': form}
        return render(request, 'exchange/calculator.html', data)

    form = CalculatorForm(request.POST)
    quantity = request.POST['currency_quantity']
    print(request.POST['currency_from'])
    print(request.POST['currency_to'])
    print(request.POST['currency_quantity'])

    data = {'form': form, 'output': 'output'}
    return render(request, 'exchange/calculator.html', data)
