from django.core.management.base import BaseCommand

from apps.partner import utils
from apps.partner.models import Currency, ExchangeRate


class Command(BaseCommand):
    def handle(self, *args, **options):
        for base_currency in Currency.objects.all():
            currencies = ','.join(Currency.objects.exclude(code=base_currency.code).values_list('code', flat=True))
            rates = utils.fetch_exchange_rates(base_currency.code, currencies=currencies)
            for rate_code, rate_value in rates['rates'].items():
                currency = Currency.objects.get(code=rate_code)
                ExchangeRate.objects.create(base_currency=base_currency, currency=currency, value=rate_value)
                self.stdout.write('Fetched rate %s to %s' % (base_currency.code, rate_code))
