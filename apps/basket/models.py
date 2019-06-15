from django.db import models

from oscar.apps.basket.abstract_models import AbstractBasket, AbstractLine
from oscar.core.utils import get_default_currency


class Basket(AbstractBasket):
    _currency = models.CharField(max_length=3, default=get_default_currency)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._currency = value

    def change_currency(self, currency):
        self.currency = currency
        self.save()

        for line in self.all_lines():
            stock_info = self.get_stock_info(line.product, options=None)
            line.price_currency = currency
            line.price_excl_tax = stock_info.price.excl_tax
            line.price_incl_tax = stock_info.price.incl_tax
            line.save()


class Line(AbstractLine):
    @property
    def purchase_info(self):
        if not hasattr(self, '_info'):
            self._info = self.basket.strategy.fetch_for_line(self, self.stockrecord, self.basket.currency)
        return self._info


from oscar.apps.basket.models import *  # noqa isort:skip
