import json
from unittest.mock import Mock

import pytest

from exchange.views import main_view


@pytest.mark.django_db
def test_main_view_records():
    response = main_view(Mock())
    assert response.status_code == 200
    response_body = json.loads(response.content)
    assert response_body == {
        "current_rates": [
            {
                "id": 1,
                "date": "2022-12-03",
                "vendor": "mono",
                "currency_a": "USD",
                "currency_b": "UAH",
                "sell": "31.0900",
                "buy": "32.5100",
            },
            {
                "id": 2,
                "date": "2023-11-11",
                "vendor": "mono",
                "currency_a": "EUR",
                "currency_b": "UAH",
                "sell": "39.3100",
                "buy": "40.5300",
            },
            {
                "id": 3,
                "date": "2021-09-10",
                "vendor": "privatbank",
                "currency_a": "USD",
                "currency_b": "UAH",
                "sell": "38.9100",
                "buy": "40.5300",
            },
            {
                "id": 4,
                "date": "2021-09-15",
                "vendor": "vkurse",
                "currency_a": "EUR",
                "currency_b": "UAH",
                "sell": "39.3100",
                "buy": "40.5300",
            },
            {
                "id": 5,
                "date": "2023-07-03",
                "vendor": "nbu",
                "currency_a": "USD",
                "currency_b": "UAH",
                "sell": "39.3100",
                "buy": "40.5300",
            },
            {
                "id": 6,
                "date": "2021-09-10",
                "vendor": "minfin",
                "currency_a": "USD",
                "currency_b": "UAH",
                "sell": "39.3100",
                "buy": "40.5300",
            },
        ]
    }
