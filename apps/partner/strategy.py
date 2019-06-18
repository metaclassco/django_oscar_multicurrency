from decimal import Decimal as D

from django.conf import settings

from oscar.apps.partner.strategy import Default as CoreDefault
from oscar.core.loading import get_class

from apps.partner.utils import convert_currency


FixedPrice = get_class('partner.prices', 'FixedPrice')


class Default(CoreDefault):
    """
    Partner strategy, that converts prices from stockrecord currency
    to user-selected currency.
    """

    def get_currency(self):
        currency = self.request.session.get('currency', None)
        currency = currency or settings.OSCAR_DEFAULT_CURRENCY
        return currency

    def convert_currency(self, stockrecord, prices):
        currency = self.get_currency()
        price_excl_tax = convert_currency(stockrecord.price_currency, currency, prices.excl_tax)
        return FixedPrice(excl_tax=price_excl_tax, currency=currency, tax=D(0))

    def pricing_policy(self, product, stockrecord):
        prices = super().pricing_policy(product, stockrecord)
        if stockrecord:
            currency = self.get_currency()
            if currency == stockrecord.price_currency:
                return prices

            return self.convert_currency(stockrecord, prices)
        return prices

    def parent_pricing_policy(self, product, stockrecord):
        prices = super().parent_pricing_policy(product, stockrecord)
        if stockrecord:
            currency = self.get_currency()
            if currency == stockrecord.price_currency:
                return prices

            return self.convert_currency(stockrecord, prices)
        return prices


class Selector(object):
    def strategy(self, request=None, user=None, **kwargs):
        return Default(request)
