from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from oscar.core.loading import get_model


Basket = get_model('basket', 'Basket')


CURRENCY_CHOICES = [('', _('Select currency'))] + [(c,) * 2 for c in settings.OSCAR_CURRENCIES]


class BasketCurrencyForm(forms.Form):
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)
