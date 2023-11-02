from django import forms

from exchange.models import Rate


class RateForm(forms.Form):
    class Meta:
        model = Rate
        fields = ["currency_from", "currency_to"]

    currency_from = forms.ChoiceField(
        choices=[("EUR", "EUR"), ("USD", "USD")], required=True, widget=forms.Select()
    )

    currency_to = forms.ChoiceField(
        choices=[("UAH", "UAH")], required=True, widget=forms.Select()
    )
