from django.views.generic import UpdateView

from oscar.core.loading import get_class


BasketCurrencyForm = get_class('basket.forms', 'BasketCurrencyForm')


class BasketCurrencyUpdateView(UpdateView):
    form_class = BasketCurrencyForm

    def get_object(self, queryset=None):
        return self.request.basket

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')
