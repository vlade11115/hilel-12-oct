import dataclasses
from abc import ABC, abstractmethod

import requests


@dataclasses.dataclass
class SellBuy:
    sell: float
    buy: float


class RateNotFound(Exception):
    pass


class ProviderBase(ABC):
    name = None

    def __init__(self, currency_from: str, currency_to: str):
        self.currency_from = currency_from
        self.currency_to = currency_to

    @abstractmethod
    def get_rate(self) -> SellBuy:
        pass


class MonoProvider(ProviderBase):
    name = "monobank"

    iso_from_country_code = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
    }

    def get_rate(self) -> SellBuy:
        url = "https://api.monobank.ua/bank/currency"
        response = requests.get(url)
        response.raise_for_status()

        currency_from_code = self.iso_from_country_code[self.currency_from]
        currency_to_code = self.iso_from_country_code[self.currency_to]

        for currency in response.json():
            if (
                    currency["currencyCodeA"] == currency_from_code
                    and currency["currencyCodeB"] == currency_to_code
            ):
                value = SellBuy(
                    sell=float(currency["rateSell"]), buy=float(currency["rateBuy"])
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )


class PrivatbankProvider(ProviderBase):
    name = "privatbank"

    def get_rate(self) -> SellBuy:
        url = "https://currate.ru/api/?get=rates&pairs=USDRUB&key=d377eb02e5c2f5d5fbef7c61ac8ed863"
        response = requests.get(url)
        response.raise_for_status()
        for currency in response.json():
            if (
                    currency["ccy"] == self.currency_from
                    and currency["base_ccy"] == self.currency_to
            ):
                value = SellBuy(
                    buy=float(currency["buy"]), sell=float(currency["sale"])
                )
                return value
        raise RateNotFound(
            f"Cannot find rate from {self.currency_from} to {self.currency_to} in provider {self.name}"
        )


class VkurseProvider(ProviderBase):
    name = "vkurse"

    iso_from_country_code = {
        "USD": "Dollar",
        "EUR": "Euro",
    }

    def get_rate(self) -> SellBuy:
        url = "https://vkurse.dp.ua/course.json"
        response = requests.get(url)
        response.raise_for_status()

        currency_from_code = self.iso_from_country_code[self.currency_from]

        for currency, data in dict(response.json()).items():
            if (
                    currency == currency_from_code
                    and self.currency_to == "UAH"
            ):
                value = SellBuy(
                    sell=float(data["sell"]), buy=float(data["buy"])
                )
                return value
        raise RateNotFound(
            f"Exchange rate not found for {self.currency_from} to {self.currency_to}"
        )


class NBUStatProvider(ProviderBase):
    name = "nbustat"

    def get_rate(self) -> SellBuy:
        url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
        response = requests.get(url)
        response.raise_for_status()

        for currency in response.json():
            if (
                    currency["cc"] == self.currency_from
                    and self.currency_to == "UAH"
            ):
                value = SellBuy(
                    sell=float(currency["rate"]), buy=float(currency["rate"])
                )
                return value
        raise RateNotFound(
            f"Exchange rate not found for {self.currency_from} to {self.currency_to}"
        )


class CurrateProvider(ProviderBase):
    name = "currate"

    def get_rate(self) -> SellBuy:
        pair = f"{self.currency_from}{self.currency_to}"
        url = f"https://currate.ru/api/?get=rates&pairs={pair}&key=d377eb02e5c2f5d5fbef7c61ac8ed863"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data is not None:
            value = SellBuy(
                sell=float(data["data"][pair]), buy=float(data["data"][pair])
            )
            return value
        raise RateNotFound(
            f"Exchange rate not found for {self.currency_from} to {self.currency_to}"
        )


PROVIDERS = [MonoProvider, PrivatbankProvider, CurrateProvider, NBUStatProvider, VkurseProvider]
