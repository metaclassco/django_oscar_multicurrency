import logging

from django.conf import settings
from django.db import IntegrityError
from django.db.models import F
from django.dispatch import receiver

from oscar.apps.analytics.receivers import _record_products_in_order, receive_order_placed
from oscar.apps.order.signals import order_placed
from oscar.core.loading import get_class

from apps.partner.utils import convert_currency

UserRecord = get_class('analytics.models', 'UserRecord')
logger = logging.getLogger('oscar.analytics')


order_placed.disconnect(receive_order_placed)


def _record_user_order(user, order):
    try:
        record = UserRecord.objects.filter(user=user)
        if order.currency == settings.OSCAR_DEFAULT_CURRENCY:
            total_spent = order.total_incl_tax
        else:
            total_spent = convert_currency(order.currency, settings.OSCAR_DEFAULT_CURRENCY, order.total_incl_tax)

        affected = record.update(
            num_orders=F('num_orders') + 1,
            num_order_lines=F('num_order_lines') + order.num_lines,
            num_order_items=F('num_order_items') + order.num_items,
            total_spent=F('total_spent') + total_spent,
            date_last_order=order.date_placed)
        if not affected:
            UserRecord.objects.create(
                user=user, num_orders=1, num_order_lines=order.num_lines,
                num_order_items=order.num_items,
                total_spent=total_spent,
                date_last_order=order.date_placed)
    except IntegrityError:      # pragma: no cover
        logger.error(
            "IntegrityError in analytics when recording a user order.")


@receiver(order_placed)
def analytics_receive_order_placed(sender, order, user, **kwargs):
    if kwargs.get('raw', False):
        return
    _record_products_in_order(order)
    if user and user.is_authenticated:
        _record_user_order(user, order)
