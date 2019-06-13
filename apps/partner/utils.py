from decimal import Decimal as D, ROUND_HALF_UP

import requests

from django.core.cache import cache

from .models import Currency, ExchangeRate


EXCHANGERATES_API_URL = 'https://api.exchangeratesapi.io/latest?base=%s&symbols=%s'
DEFAULT_CURRENCY_CACHE_KEY = 'default_currency'


def fetch_exchange_rates(base_currency, currencies):
    url = EXCHANGERATES_API_URL % (base_currency, currencies)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()


def get_default_currency():
    return Currency.objects.first()


def get_default_currency_code():
    default_currency = cache.get(DEFAULT_CURRENCY_CACHE_KEY)
    if not default_currency:
        default_currency = get_default_currency()
        cache.set(DEFAULT_CURRENCY_CACHE_KEY, default_currency)
    return default_currency


def convert_currency(from_currency, to_currency, value):
    rate = ExchangeRate.objects.filter(base_currency=from_currency, currency=to_currency).last()
    return D(rate.value * value).quantize(D('0.01'), ROUND_HALF_UP)
