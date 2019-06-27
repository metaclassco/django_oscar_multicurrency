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
    rate_value = cache.get(cache_key, None)
    if not rate_value:
        rate = ExchangeRate.objects.filter(base_currency=from_currency, currency=to_currency).last()
        rate_value = rate.value
        cache.set(cache_key, rate_value)

    value = D(rate_value * convertible_value).quantize(D('0.01'), ROUND_HALF_UP)
    return value
