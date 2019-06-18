from oscar.apps.offer.abstract_models import AbstractBenefit, AbstractCondition
from core.mixins import CurrencyMixin


class Benefit(CurrencyMixin, AbstractBenefit):
    @property
    def proxy_map(self):
        return {
            self.PERCENTAGE: get_class(
                'offer.benefits', 'PercentageDiscountBenefit'),
            self.FIXED: get_class(
                'offer.benefits', 'CurrencyAwareAbsoluteDiscountBenefit'),
            self.MULTIBUY: get_class(
                'offer.benefits', 'MultibuyDiscountBenefit'),
            self.FIXED_PRICE: get_class(
                'offer.benefits', 'CurrencyAwareFixedPriceBenefit'),
            self.SHIPPING_ABSOLUTE: get_class(
                'offer.benefits', 'CurrencyAwareShippingAbsoluteDiscountBenefit'),
            self.SHIPPING_FIXED_PRICE: get_class(
                'offer.benefits', 'CurrencyAwareShippingFixedPriceBenefit'),
            self.SHIPPING_PERCENTAGE: get_class(
                'offer.benefits', 'ShippingPercentageDiscountBenefit')
        }


class Condition(CurrencyMixin, AbstractCondition):
    @property
    def proxy_map(self):
        return {
            self.COUNT: get_class(
                'offer.conditions', 'CountCondition'),
            self.VALUE: get_class(
                'offer.conditions', 'CurrencyAwareValueCondition'),
            self.COVERAGE: get_class(
                'offer.conditions', 'CoverageCondition'),
        }


from oscar.apps.offer.models import *  # noqa isort:skip
from .benefits import *  # noqa isort:skip
from .conditions import * # noqa isort:skip
