from unittest.mock import MagicMock

import responses

from exchange.currency_provider import (
    MonoProvider,
    SellBuy,
    PrivatbankProvider,
    VkurseProvider,
    NBUProvider,
    MinfinProvider,
)


def test_mono_currency_provider():
    provider = MonoProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=31.0, buy=31.5))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.5)
    rate_mocked.assert_called()


@responses.activate
def test_mono_with_data():
    responses.get(
        "https://api.monobank.ua/bank/currency",
        json=[
            {
                "currencyCodeA": 840,
                "currencyCodeB": 980,
                "rateBuy": 31.0,
                "rateSell": 31.0,
            }
        ],
    )
    provider = MonoProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.0)


def test_privatbank_currency_provider():
    provider = PrivatbankProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=31.0, buy=31.5))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.5)
    rate_mocked.assert_called()


@responses.activate
def test_privatbank_with_data():
    responses.get(
        "https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5",
        json=[
            {
                "ccy": "EUR",
                "base_ccy": "UAH",
                "buy": 31.0,
                "sale": 31.0,
            },
            {
                "ccy": "USD",
                "base_ccy": "UAH",
                "buy": 31.0,
                "sale": 31.0,
            },
        ],
    )
    provider = PrivatbankProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.0)


def test_vkurse_currency_provider():
    provider = VkurseProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=31.0, buy=31.5))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.5)
    rate_mocked.assert_called()


@responses.activate
def test_vkurse_with_data():
    responses.get(
        "https://vkurse.dp.ua/course.json",
        json={
            "Dollar": {"buy": "31.0", "sale": "31.0"},
            "Euro": {"buy": "31.0", "sale": "31.0"},
        },
    )
    provider = VkurseProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.0)


def test_nbu_currency_provider():
    provider = NBUProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=31.0, buy=31.5))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.5)
    rate_mocked.assert_called()


@responses.activate
def test_nbu_with_data():
    responses.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",
        json=[
            {
                "cc": "EUR",
                "rate": 31.0,
            },
            {
                "cc": "USD",
                "rate": 31.0,
            },
        ],
    )
    provider = NBUProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.0)


def test_minfin_currency_provider():
    provider = MinfinProvider("USD", "UAH")
    rate_mocked = MagicMock(return_value=SellBuy(sell=31.0, buy=31.5))
    provider.get_rate = rate_mocked
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.5)
    rate_mocked.assert_called()


@responses.activate
def test_minfin_with_data():
    responses.get(
        "https://api.minfin.com.ua/mb/2d57c01794142f530091b1330cfbbbf19d4c2dee/",
        json=[
            {
                "currency": "usd",
                "ask": 31.0,
                "bid": 31.0,
            },
            {
                "currency": "eur",
                "ask": 31.0,
                "bid": 31.0,
            },
        ],
    )
    provider = MinfinProvider("USD", "UAH")
    rate = provider.get_rate()
    assert rate == SellBuy(sell=31.0, buy=31.0)
