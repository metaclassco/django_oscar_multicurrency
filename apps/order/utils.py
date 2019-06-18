from django.conf import settings

from oscar.apps.order.utils import OrderCreator as CoreOrderCreator
from oscar.core.loading import get_model

from apps.partner.utils import convert_currency


Order = get_model('order', 'Order')
Line = get_model('order', 'Line')
OrderDiscount = get_model('order', 'OrderDiscount')


class OrderCreator(CoreOrderCreator):
    def create_discount_model(self, order, discount):
        offer = discount['offer']
        benefit = offer.benefit
        if benefit.currency != settings.OSCAR_DEFAULT_CURRENCY:
            amount = discount['discount']
            discount['discount'] = convert_currency(benefit.currency, settings.OSCAR_DEFAULT_CURRENCY, amount)
        super().create_discount_model(order, discount)
