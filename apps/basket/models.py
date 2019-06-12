from django.db import models
from oscar.apps.basket.abstract_models import AbstractBasket


class Basket(AbstractBasket):
    currency = models.ForeignKey(
        'partner.Currency', on_delete=models.CASCADE, related_name='baskets', null=True, blank=True
    )


from oscar.apps.basket.models import *  # noqa isort:skip
