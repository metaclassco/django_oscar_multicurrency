from django.conf import settings

from oscar.apps.shipping.repository import Repository as CoreRepository

from .methods import FixedPrice


class Repository(CoreRepository):
    methods = (FixedPrice(),)
    currency = settings.OSCAR_DEFAULT_CURRENCY
