from django.http import JsonResponse
from django.shortcuts import render

from .forms import RateForm
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


def calculate_currency(request):
    best_rate = None
    if request.method == "GET":
        form = RateForm()
        return render(
            request, "calculate_form.html", {"currency": form, "best_rate": best_rate}
        )

    if request.method == "POST":
        form = RateForm(request.POST)
        if form.is_valid():
            currency_from = form.cleaned_data["currency_from"]
            currency_to = form.cleaned_data["currency_to"]

            best_rate = (
                Rate.objects.filter(
                    currency_from=currency_from, currency_to=currency_to
                )
                .order_by("buy")
                .first()
            )

        return render(
            request, "calculate_form.html", {"currency": form, "best_rate": best_rate}
        )
