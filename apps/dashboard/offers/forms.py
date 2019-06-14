from django import forms
from django.conf import settings

from oscar.apps.dashboard.offers.forms import BenefitForm as CoreBenefitForm
from oscar.apps.dashboard.offers.forms import ConditionForm as CoreConditionForm


CURRENCY_CHOICES = [(c,) * 2 for c in settings.OSCAR_CURRENCIES]


class CurrencyFormMixin(forms.Form):
    currency = forms.ChoiceField(choices=CURRENCY_CHOICES)


class BenefitForm(CurrencyFormMixin, CoreBenefitForm):

    class Meta(CoreBenefitForm.Meta):
        fields = ['range', 'type', 'value', 'max_affected_items', 'currency']


class ConditionForm(CurrencyFormMixin, CoreConditionForm):
    class Meta(CoreConditionForm.Meta):
        fields = ['range', 'type', 'value', 'currency']
