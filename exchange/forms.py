from django import forms


class CurrencyExchangeForm(forms.Form):
    currency_sell = forms.ChoiceField(
        choices=[("USD", "USD"), ("UAH", "UAH"), ("EUR", "EUR")], label="Ваша валюта"
    )
    currency_buy = forms.ChoiceField(
        choices=[("USD", "USD"), ("UAH", "UAH"), ("EUR", "EUR")],
        label="Отримана валюта",
    )
    suma = forms.DecimalField(
        label="Сума", min_value=0, max_digits=10, decimal_places=2
    )
