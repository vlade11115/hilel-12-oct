from django import forms


CURRENCY_CHOICES = [
    ('EUR', 'EUR'),
    ('UAH', 'UAH'),
    ('USD', 'USD'),
]


class CalculatorForm(forms.Form):
    currency_from = forms.ChoiceField(choices=CURRENCY_CHOICES)
    currency_to = forms.ChoiceField(choices=CURRENCY_CHOICES)
    currency_quantity = forms.CharField(max_length=4)
