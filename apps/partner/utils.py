from decimal import Decimal as D, ROUND_HALF_UP

import requests

from django.core.cache import cache

from .models import ExchangeRate


EXCHANGERATES_API_URL = 'https://api.exchangeratesapi.io/latest?base=%s&symbols=%s'
EXCHANGE_RATE_CACHE_KEY = '%s-%s_rate'


def fetch_exchange_rates(base_currency, currencies):
    url = EXCHANGERATES_API_URL % (base_currency, currencies)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()


def convert_currency(from_currency, to_currency, convertible_value):
    cache_key = EXCHANGE_RATE_CACHE_KEY % (from_currency, to_currency)
    value = cache.get(cache_key, None)
    if value:
        return value

    rate = ExchangeRate.objects.filter(base_currency=from_currency, currency=to_currency).last()
    value = D(rate.value * convertible_value).quantize(D('0.01'), ROUND_HALF_UP)
    cache.set(cache_key, value)
    return value
