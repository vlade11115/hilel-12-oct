import datetime

from django.db.models import Max, Min
from django.http import JsonResponse
from django.shortcuts import render

from .forms import CurrencyExchangeForm
from .models import Rate


def exchange_rates(request):
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


def currency_exchange_calculator(request):
    rates = Rate.objects.filter(date=datetime.date.today())

    if not rates.exists():
        form = CurrencyExchangeForm()
        error = f"База даних порожня обмін не можливий"
        return render(
            request,
            "currency_exchange_calculator.html",
            {"error": error, "rates": rates, "form": form},
        )

    if request.method == "GET":
        form = CurrencyExchangeForm()
        return render(
            request, "currency_exchange_calculator.html", {"form": form, "rates": rates}
        )
    form = CurrencyExchangeForm(request.POST)

    if form.is_valid():
        currency_sell = form.cleaned_data["currency_sell"]
        currency_buy = form.cleaned_data["currency_buy"]
        suma = form.cleaned_data["suma"]

        if currency_sell == currency_buy:
            form.add_error("currency_sell", "Неможливо конвертувати однакові валюти!")
            return render(
                request,
                "currency_exchange_calculator.html",
                {"form": form, "rates": rates},
            )

        if currency_sell != "UAH" and currency_buy != "UAH":
            form.add_error(
                "currency_sell",
                f"Наш обмінник не може конвертувати {currency_sell} в {currency_buy}",
            )
            return render(
                request,
                "currency_exchange_calculator.html",
                {"form": form, "rates": rates},
            )

        if currency_sell == "UAH":
            rate = rates.filter(currency_from=currency_buy).aggregate(Min("sell"))[
                "sell__min"
            ]
            if not rate:
                form = CurrencyExchangeForm()
                error = f"На даний момент в цю валюту конвертувати не можливо"
                return render(
                    request,
                    "currency_exchange_calculator.html",
                    {"error": error, "rates": rates, "form": form},
                )
            result = round(float(suma / rate), 2)
            return render(
                request,
                "currency_exchange_calculator.html",
                {
                    "form": form,
                    "rates": rates,
                    "result": result,
                    "suma": suma,
                    "currency_sell": currency_sell,
                    "currency_buy": currency_buy,
                },
            )
        if currency_buy == "UAH":
            rate = rates.filter(currency_from=currency_sell).aggregate(Max("buy"))[
                "buy__max"
            ]
            if not rate:
                form = CurrencyExchangeForm()
                error = f"На даний момент з цієї валюти конвертувати не можливо"
                return render(
                    request,
                    "currency_exchange_calculator.html",
                    {"error": error, "rates": rates, "form": form},
                )
            result = round(float(suma * rate), 2)
            return render(
                request,
                "currency_exchange_calculator.html",
                {
                    "form": form,
                    "rates": rates,
                    "result": result,
                    "suma": suma,
                    "currency_sell": currency_sell,
                    "currency_buy": currency_buy,
                },
            )
