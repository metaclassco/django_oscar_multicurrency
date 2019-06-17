from decimal import Decimal as D

from oscar.apps.offer.benefits import (
    AbsoluteDiscountBenefit, FixedPriceBenefit, ShippingAbsoluteDiscountBenefit, ShippingFixedPriceBenefit)
from oscar.apps.offer.benefits import apply_discount
from oscar.apps.offer.conditions import CoverageCondition, ValueCondition
from oscar.apps.offer.results import ZERO_DISCOUNT, BasketDiscount
from oscar.core.loading import get_class
from oscar.templatetags.currency_filters import currency
from apps.partner.utils import convert_currency

range_anchor = get_class('offer.utils', 'range_anchor')


class CurrencyAwareAbsoluteDiscountBenefit(AbsoluteDiscountBenefit):
    @property
    def name(self):
        return self._description % {
            'value': currency(self.value, self.currency),
            'range': self.range.name.lower()}

    @property
    def description(self):
        return self._description % {
            'value': currency(self.value, self.currency),
            'range': range_anchor(self.range)}

    def apply(self,  basket, condition, offer, **kwargs):
        if basket.currency != self.currency:
            discount_amount = kwargs.get('discount_amount', self.value)
            kwargs['discount_amount'] = convert_currency(self.currency, basket.currency, discount_amount)
        return super().apply(basket, condition, offer, **kwargs)


class CurrencyAwareFixedPriceBenefit(FixedPriceBenefit):
    @property
    def name(self):
        return self._description % {
            'amount': currency(self.value, self.currency)}


class CurrencyAwareShippingAbsoluteDiscountBenefit(ShippingAbsoluteDiscountBenefit):
    @property
    def name(self):
        return self._description % {
            'amount': currency(self.value, self.currency)}


class CurrencyAwareShippingFixedPriceBenefit(ShippingFixedPriceBenefit):
    @property
    def name(self):
        return self._description % {
            'amount': currency(self.value, self.currency)}
