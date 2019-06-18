from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from oscar.apps.basket.middleware import BasketMiddleware as CoreBasketMiddleware
from oscar.core.loading import get_model

Basket = get_model('basket', 'basket')


class BasketMiddleware(CoreBasketMiddleware):
    def get_basket(self, request):
        if request._basket_cache is not None:
            return request._basket_cache

        num_baskets_merged = 0
        manager = Basket.open
        cookie_key = self.get_cookie_key(request)
        cookie_basket = self.get_cookie_basket(cookie_key, request, manager)

        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                basket, created = manager.get_or_create(owner=request.user)
                if created:
                    basket.currency = request.session.get('currency', settings.OSCAR_DEFAULT_CURRENCY)
                    basket.save()
            except Basket.MultipleObjectsReturned:
                old_baskets = list(manager.filter(owner=request.user))
                basket = old_baskets[0]
                for other_basket in old_baskets[1:]:
                    self.merge_baskets(basket, other_basket)
                    num_baskets_merged += 1

            basket.owner = request.user

            if cookie_basket:
                self.merge_baskets(basket, cookie_basket)
                num_baskets_merged += 1
                request.cookies_to_delete.append(cookie_key)

        elif cookie_basket:
            basket = cookie_basket
        else:
            basket = Basket()

        request._basket_cache = basket

        if num_baskets_merged > 0:
            messages.add_message(request, messages.WARNING,
                                 _("We have merged a basket from a previous session. Its contents "
                                   "might have changed."))

        return basket
