from oscar.apps.offer.conditions import ValueCondition
from oscar.core.loading import get_class
from oscar.templatetags.currency_filters import currency

range_anchor = get_class('offer.utils', 'range_anchor')


class CurrencyAwareValueCondition(ValueCondition):
    @property
    def name(self):
        return self._description % {
            'amount': currency(self.value, self.currency),
            'range': str(self.range).lower()}

    @property
    def description(self):
        return self._description % {
            'amount': currency(self.value, self.currency),
            'range': range_anchor(self.range)}
