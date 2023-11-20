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
                "date": "2021-01-01",
                "vendor": "mono",
                "currency_a": "USD",
                "currency_b": "UAH",
                "sell": "30.0000",
                "buy": "34.0000",
            },
            {
                "id": 2,
                "date": "2023-11-05",
                "vendor": "mono",
                "currency_a": "USD",
                "currency_b": "UAH",
                "sell": "37.2995",
                "buy": "36.1400",
            },
        ]
    }
