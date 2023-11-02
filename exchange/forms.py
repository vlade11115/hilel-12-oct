from django import forms

CURRENCY_CHOICES = [
    ("EUR", "EUR"),
    ("USD", "USD"),
]

CURRENCY_CHOICES_TO = [
    ("UAH", "UAH"),
]

OPERATION_CHOICES = [
    ("buy", "buy"),
    ("sell", "sell"),
]


class CalculatorForm(forms.Form):
    currency_from = forms.ChoiceField(choices=CURRENCY_CHOICES)
    currency_quantity = forms.CharField(max_length=4)
    currency_to = forms.ChoiceField(choices=CURRENCY_CHOICES_TO)
    operation = forms.ChoiceField(choices=OPERATION_CHOICES)
