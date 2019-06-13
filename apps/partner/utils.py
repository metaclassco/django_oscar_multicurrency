from decimal import Decimal as D, ROUND_HALF_UP

import requests

from .models import ExchangeRate


EXCHANGERATES_API_URL = 'https://api.exchangeratesapi.io/latest?base=%s&symbols=%s'
DEFAULT_CURRENCY_CACHE_KEY = 'default_currency'


def fetch_exchange_rates(base_currency, currencies):
    url = EXCHANGERATES_API_URL % (base_currency, currencies)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()


def convert_currency(from_currency, to_currency, value):
    rate = ExchangeRate.objects.filter(base_currency=from_currency, currency=to_currency).last()
    return D(rate.value * value).quantize(D('0.01'), ROUND_HALF_UP)
