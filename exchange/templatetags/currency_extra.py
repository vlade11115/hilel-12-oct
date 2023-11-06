from django import template

register = template.Library()

currency_to_ukrainian = {
    "USD": "Долар США",
    "EUR": "Євро",
    "UAH": "Гривня",
}

currency_to_simbols = {
    "USD": "$",
    "EUR": "€",
    "UAH": "₴",
}


@register.filter(name="humanize_currency")
def humanize_currency(value):
    return currency_to_ukrainian.get(value, value)


@register.filter(name="symbolize_currency")
def symbolize_currency(value):
    return currency_to_simbols.get(value, value)
