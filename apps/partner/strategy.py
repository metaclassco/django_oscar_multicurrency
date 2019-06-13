from decimal import Decimal as D
from oscar.apps.partner.strategy import Default as CoreDefault
from oscar.core.loading import get_class

from apps.partner.utils import convert_currency, get_default_currency_code


FixedPrice = get_class('partner.prices', 'FixedPrice')


class Default(CoreDefault):
    def convert_currency(self, stockrecord, prices):
        base_currency = self.request.basket.currency or get_default_currency_code()
        price_excl_tax = convert_currency(stockrecord.price_currency, base_currency, prices.excl_tax)
        return FixedPrice(excl_tax=price_excl_tax, currency=self.request.basket.currency, tax=D(0))

    def pricing_policy(self, product, stockrecord):
        prices = super().pricing_policy(product, stockrecord)
        base_currency = self.request.basket.currency or get_default_currency_code()
        if base_currency == stockrecord.price_currency:
            return prices

        return self.convert_currency(stockrecord, prices)

    def parent_pricing_policy(self, product, stockrecord):
        prices = super().parent_pricing_policy(product, stockrecord)
        if self.request.basket.currency == stockrecord.price_currency:
            return prices

        return self.convert_currency(stockrecord, prices)


class Selector(object):
    def strategy(self, request=None, user=None, **kwargs):
        return Default(request)
