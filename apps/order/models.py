from django.db import models

from oscar.apps.order.abstract_models import AbstractOrder


class Order(AbstractOrder):
    currency = models.ForeignKey('partner.Currency', on_delete=models.CASCADE, related_name='orders')


from oscar.apps.order.models import *  # noqa isort:skip
