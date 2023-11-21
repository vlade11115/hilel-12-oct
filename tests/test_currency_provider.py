from unittest.mock import MagicMock

import responses

from exchange.currency_provider import (
    MonoProvider,
    PrivatbankProvider,
    NBUProvider,
    VkurseProvider,
    MinfinProvider,
    SellBuy,
)

""" Tests with MagicMock """


def test_mono_currency_provider():
    provider_usd = MonoProvider("USD", "UAH")
    provider_eur = MonoProvider("EUR", "UAH")
    rate_mocked_usd = MagicMock(return_value=SellBuy(sell=27.0, buy=27.0))
    rate_mocked_eur = MagicMock(return_value=SellBuy(sell=30.0, buy=30.0))

    provider_usd.get_rate = rate_mocked_usd
    provider_eur.get_rate = rate_mocked_eur
    rate_usd = provider_usd.get_rate()
    rate_eur = provider_eur.get_rate()

    assert rate_usd == SellBuy(sell=27.0, buy=27.0)
    assert rate_eur == SellBuy(sell=30.0, buy=30.0)
    rate_mocked_usd.assert_called()
    rate_mocked_eur.assert_called()


def test_privatbank_currency_provider():
    provider_usd = PrivatbankProvider("USD", "UAH")
    provider_eur = PrivatbankProvider("EUR", "UAH")
    rate_mocked_usd = MagicMock(return_value=SellBuy(sell=29.0, buy=27.0))
    rate_mocked_eur = MagicMock(return_value=SellBuy(sell=31.0, buy=30.0))

    provider_usd.get_rate = rate_mocked_usd
    provider_eur.get_rate = rate_mocked_eur
    rate_usd = provider_usd.get_rate()
    rate_eur = provider_eur.get_rate()

    assert rate_usd == SellBuy(sell=29.0, buy=27.0)
    assert rate_eur == SellBuy(sell=31.0, buy=30.0)
    rate_mocked_usd.assert_called()
    rate_mocked_eur.assert_called()


def test_nbu_currency_provider():
    provider_usd = NBUProvider("USD", "UAH")
    provider_eur = NBUProvider("EUR", "UAH")
    rate_mocked_usd = MagicMock(return_value=SellBuy(sell=25.0, buy=25.0))
    rate_mocked_eur = MagicMock(return_value=SellBuy(sell=29.0, buy=29.0))

    provider_usd.get_rate = rate_mocked_usd
    provider_eur.get_rate = rate_mocked_eur
    rate_usd = provider_usd.get_rate()
    rate_eur = provider_eur.get_rate()

    assert rate_usd == SellBuy(sell=25.0, buy=25.0)
    assert rate_eur == SellBuy(sell=29.0, buy=29.0)
    rate_mocked_usd.assert_called()
    rate_mocked_eur.assert_called()


""" Tests with responses"""


@responses.activate
def test_mono_with_data():
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=[
            {
                "currencyCodeA": 840,
                "currencyCodeB": 980,
                "rateBuy": 28.0,
                "rateSell": 28.0,
            },
            {
                "currencyCodeA": 978,
                "currencyCodeB": 980,
                "rateBuy": 39.42,
                "rateSell": 40.8,
            },
        ],
    )

    provider_usd = MonoProvider("USD", "UAH")
    provider_eur = MonoProvider("EUR", "UAH")
    rate_usd = provider_usd.get_rate()
    rate_eur = provider_eur.get_rate()

    assert rate_usd == SellBuy(sell=28.0, buy=28.0)
    assert rate_eur == SellBuy(sell=40.8, buy=39.42)


@responses.activate
def test_privatbank_with_data():
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5",
        json=[
            {"ccy": "USD", "base_ccy": "UAH", "buy": 37.0, "sale": 37.5},
            {
                "ccy": "EUR",
                "base_ccy": "UAH",
                "buy": 40.05,
                "sale": 41.05,
            },
        ],
    )

    provider_usd = PrivatbankProvider("USD", "UAH")
    provider_eur = PrivatbankProvider("EUR", "UAH")
    rate_usd = provider_usd.get_rate()
    rate_eur = provider_eur.get_rate()

    assert rate_usd == SellBuy(sell=37.5, buy=37.0)
    assert rate_eur == SellBuy(sell=41.05, buy=40.05)


@responses.activate
def test_nbu_with_data():
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
        json=[
            {
                "r030": 840,
                "rate": 36.04,
            },
            {
                "r030": 978,
                "rate": 39.39,
            },
        ],
    )

    provider_usd = NBUProvider("USD", "UAH")
    provider_eur = NBUProvider("EUR", "UAH")
    rate_usd = provider_usd.get_rate()
    rate_eur = provider_eur.get_rate()

    assert rate_usd == SellBuy(sell=36.04, buy=36.04)
    assert rate_eur == SellBuy(sell=39.39, buy=39.39)


@responses.activate
def test_vkurse_with_data():
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json={
            "Dollar": {"buy": 37.65, "sale": 37.90},
            "Euro": {"buy": 40.90, "sale": 41.10},
        },
    )

    provider_usd = VkurseProvider("USD", "UAH")
    provider_eur = VkurseProvider("EUR", "UAH")
    rate_usd = provider_usd.get_rate()
    rate_eur = provider_eur.get_rate()

    assert rate_usd == SellBuy(sell=37.90, buy=37.65)
    assert rate_eur == SellBuy(sell=41.10, buy=40.90)


@responses.activate
def test_minfin_with_data():
    responses.get(
        "https://minfin.com.ua/api/currency/simple/?base=UAH&list=usd,eur",
        json={
            "data": {
                "USD": {
                    "midbank": {
                        "buy": {
                            "val": 37.35,
                        },
                        "sell": {"val": 37.8},
                    }
                },
                "EUR": {
                    "midbank": {
                        "buy": {
                            "val": 40.4,
                        },
                        "sell": {
                            "val": 41.05,
                        },
                    }
                },
            }
        },
    )

    provider_usd = MinfinProvider("USD", "UAH")
    provider_eur = MinfinProvider("EUR", "UAH")
    rate_usd = provider_usd.get_rate()
    rate_eur = provider_eur.get_rate()

    assert rate_usd == SellBuy(sell=37.8, buy=37.35)
    assert rate_eur == SellBuy(sell=41.05, buy=40.4)
