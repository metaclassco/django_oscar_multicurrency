from decimal import Decimal as D

from django.utils.translation import gettext_lazy as _

from oscar.apps.offer.conditions import ValueCondition
from oscar.core.loading import get_classes
from oscar.templatetags.currency_filters import currency

from apps.partner.utils import convert_currency

range_anchor, unit_price = get_classes('offer.utils', ['range_anchor', 'unit_price'])


class CurrencyAwareValueCondition(ValueCondition):
    class Meta(ValueCondition.Meta):
        proxy = True

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

    def get_condition_value(self, basket):
        if self.currency != basket.currency:
            return convert_currency(self.currency, basket.currency, self.value)
        return self.value

    def is_satisfied(self, offer, basket):
        value_of_matches = D('0.00')
        for line in basket.all_lines():
            if (self.can_apply_condition(line)
                    and line.quantity_without_offer_discount(offer) > 0):
                price = unit_price(offer, line)
                value_of_matches += price * int(
                    line.quantity_without_offer_discount(offer)
                )

            if value_of_matches >= self.get_condition_value(basket):
                return True
        return False

    def is_partially_satisfied(self, offer, basket):
        value_of_matches = self._get_value_of_matches(offer, basket)
        return D('0.00') < value_of_matches < self.get_condition_value(basket)

    def get_upsell_message(self, offer, basket):
        value_of_matches = self._get_value_of_matches(offer, basket)
        condition_value = self.get_condition_value(basket)
        return _('Spend %(value)s more from %(range)s') % {
            'value': currency(condition_value - value_of_matches, self.currency),
            'range': self.range}
