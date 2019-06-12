import requests

from django.core.cache import cache

from .models import Currency


EXCHANGERATES_API_URL = 'https://api.exchangeratesapi.io/latest?base=%s&symbols=%s'
DEFAULT_CURRENCY_CACHE_KEY = 'default_currency'


def fetch_exchange_rates(base_currency, currencies):
    url = EXCHANGERATES_API_URL % (base_currency, currencies)
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()


def get_default_currency():
    default_currency = cache.get(DEFAULT_CURRENCY_CACHE_KEY)
    if not default_currency:
        currency = Currency.objects.first()
        default_currency = currency.code
        cache.set(DEFAULT_CURRENCY_CACHE_KEY, default_currency)
    return default_currency
