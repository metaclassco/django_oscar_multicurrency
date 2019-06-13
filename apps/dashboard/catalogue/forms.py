from django import forms
from django.conf import settings

from oscar.apps.dashboard.catalogue.forms import StockRecordForm as CoreStockRecordForm


CURRENCY_CHOICES = [(c,) * 2 for c in settings.OSCAR_CURRENCIES]


class StockRecordForm(CoreStockRecordForm):
    price_currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
