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
    class Meta(AbsoluteDiscountBenefit.Meta):
        proxy = True

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
    class Meta(FixedPriceBenefit.Meta):
        proxy = True

    def get_benefit_value(self, basket):
        if self.currency != basket.currency:
            return convert_currency(self.currency, basket.currency, self.value)
        return self.value

    @property
    def name(self):
        return self._description % {
            'amount': currency(self.value, self.currency)}

    def apply(self, basket, condition, offer, **kwargs):  # noqa (too complex (10))
        if isinstance(condition, ValueCondition):
            return ZERO_DISCOUNT

        benefit_value = self.get_benefit_value(basket)
        line_tuples = self.get_applicable_lines(offer, basket, range=condition.range)
        if not line_tuples:
            return ZERO_DISCOUNT

        # Determine the lines to consume
        num_permitted = int(condition.value)
        num_affected = 0
        value_affected = D('0.00')
        covered_lines = []
        for price, line in line_tuples:
            if isinstance(condition, CoverageCondition):
                quantity_affected = 1
            else:
                quantity_affected = min(
                    line.quantity_without_offer_discount(offer),
                    num_permitted - num_affected)
            num_affected += quantity_affected
            value_affected += quantity_affected * price
            covered_lines.append((price, line, quantity_affected))
            if num_affected >= num_permitted:
                break

        discount = max(value_affected - benefit_value, D('0.00'))
        if not discount:
            return ZERO_DISCOUNT

        discount_applied = D('0.00')
        last_line = covered_lines[-1][1]
        for price, line, quantity in covered_lines:
            if line == last_line:
                line_discount = discount - discount_applied
            else:
                line_discount = self.round(
                    discount * (price * quantity) / value_affected)
            apply_discount(line, line_discount, quantity, offer)
            discount_applied += line_discount
        return BasketDiscount(discount)


class CurrencyAwareShippingAbsoluteDiscountBenefit(ShippingAbsoluteDiscountBenefit):
    class Meta(ShippingAbsoluteDiscountBenefit.Meta):
        proxy = True

    @property
    def name(self):
        return self._description % {
            'amount': currency(self.value, self.currency)}


class CurrencyAwareShippingFixedPriceBenefit(ShippingFixedPriceBenefit):
    class Meta(ShippingFixedPriceBenefit.Meta):
        proxy = True

    @property
    def name(self):
        return self._description % {
            'amount': currency(self.value, self.currency)}
