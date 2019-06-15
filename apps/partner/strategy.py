from decimal import Decimal as D

from django.conf import settings

from oscar.apps.partner.strategy import Default as CoreDefault
from oscar.core.loading import get_class

from apps.partner.utils import convert_currency


FixedPrice = get_class('partner.prices', 'FixedPrice')


class Default(CoreDefault):
    currency = None

    def fetch_for_line(self, line, stockrecord=None, currency=None):
        self.currency = currency
        return self.fetch_for_product(line.product)

    def convert_currency(self, stockrecord, prices):
        basket_currency = self.currency or self.request.basket.currency or settings.OSCAR_DEFAULT_CURRENCY
        price_excl_tax = convert_currency(stockrecord.price_currency, basket_currency, prices.excl_tax)
        return FixedPrice(excl_tax=price_excl_tax, currency=basket_currency, tax=D(0))

    def pricing_policy(self, product, stockrecord):
        prices = super().pricing_policy(product, stockrecord)
        if stockrecord:
            basket_currency = self.currency or self.request.basket.currency or settings.OSCAR_DEFAULT_CURRENCY
            if basket_currency == stockrecord.price_currency:
                return prices

            return self.convert_currency(stockrecord, prices)
        return prices

    def parent_pricing_policy(self, product, stockrecord):
        prices = super().parent_pricing_policy(product, stockrecord)
        if stockrecord:
            basket_currency = self.currency or self.request.basket.currency or settings.OSCAR_DEFAULT_CURRENCY
            if basket_currency == stockrecord.price_currency:
                return prices

            return self.convert_currency(stockrecord, prices)
        return prices


class Selector(object):
    def strategy(self, request=None, user=None, **kwargs):
        return Default(request)
