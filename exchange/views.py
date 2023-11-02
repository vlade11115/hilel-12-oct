from datetime import datetime

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
    today = datetime.now().date()

    if request.method == "GET":
        form = CalculatorForm()
        data = {"form": form}
        return render(request, "exchange/calculator.html", data)

    form = CalculatorForm(request.POST)

    quantity = int(request.POST["currency_quantity"])
    currency_from = request.POST["currency_from"]
    operation = request.POST["operation"]

    all_providers = []
    provider_info = (
        Rate.objects.filter(date=today, currency_from=currency_from)
        .values("provider", operation)
        .order_by(operation)
    )
    for provider in provider_info:
        all_providers.append(
            [provider["provider"], float(provider[operation]) * quantity]
        )

    best_provider = (
        Rate.objects.filter(date=today, currency_from=currency_from)
        .order_by(operation)
        .first()
    )
    if operation == "buy":
        output = float(best_provider.buy) * quantity
    else:
        output = float(best_provider.sell) * quantity

    data = {
        "form": form,
        "all_providers": all_providers,
        "output": output,
        "today": today,
    }
    return render(request, "exchange/calculator.html", data)
