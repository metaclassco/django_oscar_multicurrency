from oscar.apps.offer.benefits import (
    AbsoluteDiscountBenefit, FixedPriceBenefit, ShippingAbsoluteDiscountBenefit, ShippingFixedPriceBenefit)
from oscar.core.loading import get_class
from oscar.templatetags.currency_filters import currency

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
