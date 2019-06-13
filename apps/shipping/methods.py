from decimal import Decimal as D

from django.conf import settings

from oscar.apps.shipping.methods import FixedPrice as OriginalFixedPrice
from oscar.core import prices

from apps.partner.utils import convert_currency


class FixedPrice(OriginalFixedPrice):
    charge_incl_tax = D(10)
    charge_excl_tax = D(10)
    currency = settings.OSCAR_DEFAULT_CURRENCY

    def __init__(self, charge_excl_tax=None, charge_incl_tax=None, currency=None):
        super().__init__(charge_excl_tax=charge_excl_tax, charge_incl_tax=charge_incl_tax)
        if currency:
            self.currency = currency

    def calculate(self, basket):
        if self.currency == basket.currency:
            return super().calculate(basket)

        charge_excl_tax = convert_currency(self.currency, basket.currency, self.charge_excl_tax)
        charge_incl_tax = convert_currency(self.currency, basket.currency, self.charge_incl_tax)
        return prices.Price(
            currency=self.currency,
            excl_tax=charge_excl_tax,
            incl_tax=charge_incl_tax)
