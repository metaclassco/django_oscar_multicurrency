from django.conf import settings

from oscar.apps.order.abstract_models import AbstractOrder

from apps.partner.utils import convert_currency


class Order(AbstractOrder):
    @property
    def is_in_default_currency(self):
        return self.currency == settings.OSCAR_DEFAULT_CURRENCY

    def convert_to_default_currency(self, property_name):
        value = getattr(self, property_name, '')
        if not self.is_in_default_currency and value:
            return convert_currency(self.currency, settings.OSCAR_DEFAULT_CURRENCY, value)
        return value

    @property
    def total_incl_tax_in_default_currency(self):
        return self.convert_to_default_currency('total_incl_tax')

    @property
    def shipping_incl_tax_in_default_currency(self):
        return self.convert_to_default_currency('shipping_incl_tax')

    @property
    def shipping_excl_tax_in_default_currency(self):
        return self.convert_to_default_currency('shipping_excl_tax')


from oscar.apps.order.models import *  # noqa isort:skip
