from django.db import models

from oscar.apps.partner.abstract_models import AbstractStockRecord


class Currency(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3, primary_key=True)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    base_currency = models.ForeignKey('Currency', related_name='base_currencies', on_delete=models.CASCADE)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=20, decimal_places=6)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s to %s' % (self.base_currency, self.currency)


class StockRecord(AbstractStockRecord):
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)


from oscar.apps.partner.models import *  # noqa isort:skip
