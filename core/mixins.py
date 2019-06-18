from django.db import models

from oscar.core.utils import get_default_currency


class CurrencyMixin(models.Model):
    currency = models.CharField(max_length=3, default=get_default_currency)

    class Meta:
        abstract = True
