from django.db import models
from oscar.apps.basket.abstract_models import AbstractBasket, AbstractLine

from apps.partner.utils import get_default_currency


class Basket(AbstractBasket):
    currency = models.ForeignKey(
        'partner.Currency', on_delete=models.CASCADE, related_name='baskets', null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.currency:
            self.currency = get_default_currency()
        super().save(*args, **kwargs)


class Line(AbstractLine):
    price_currency = models.ForeignKey(
        'partner.Currency', on_delete=models.CASCADE, related_name='basket_lines', null=True, blank=True
    )


from oscar.apps.basket.models import *  # noqa isort:skip
