import oscar.apps.basket.apps as apps


class BasketConfig(apps.BasketConfig):
    label = 'basket'
    name = 'apps.basket'
    verbose_name = 'Cart'
