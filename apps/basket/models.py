from oscar.apps.basket.abstract_models import AbstractBasket


class Basket(AbstractBasket):
    def change_currency(self, currency):
        for line in self.lines.all():
            line.price_currency = currency
            line.save()


from oscar.apps.basket.models import *  # noqa isort:skip
