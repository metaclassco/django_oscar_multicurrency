from django.http import HttpResponseRedirect
from django.views.generic import FormView

from oscar.core.loading import get_class


BasketCurrencyForm = get_class('basket.forms', 'BasketCurrencyForm')


class BasketCurrencyUpdateView(FormView):
    form_class = BasketCurrencyForm

    def form_valid(self, form):
        currency = form.cleaned_data['currency']
        self.request.basket.change_currency(currency)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')
