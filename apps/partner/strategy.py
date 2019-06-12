from oscar.apps.partner.strategy import Default as CoreDefault
from oscar.core.loading import get_class

from apps.partner.utils import convert_currency


FixedPrice = get_class('partner.prices', 'FixedPrice')


class Default(CoreDefault):
    def convert_currency(self, stockrecord, prices):
        price_excl_tax = convert_currency(
            stockrecord.price_currency, self.request.basket.currency, prices.excl_tax
        )
        return FixedPrice(excl_tax=price_excl_tax, currency=self.request.basket.currency)

    def pricing_policy(self, product, stockrecord):
        prices = super().pricing_policy(product, stockrecord)
        if self.request.basket.currency == stockrecord.price_currency:
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
