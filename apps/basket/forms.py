from django import forms
from django.utils.translation import gettext_lazy as _

from oscar.core.loading import get_model


Basket = get_model('basket', 'Basket')
Currency = get_model('partner', 'Currency')


class BasketCurrencyForm(forms.ModelForm):
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), empty_label=_('Select currency'))

    class Meta:
        model = Basket
        fields = ('currency',)
