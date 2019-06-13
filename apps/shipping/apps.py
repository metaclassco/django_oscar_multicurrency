import oscar.apps.shipping.apps as apps


class ShippingConfig(apps.ShippingConfig):
    label = 'shipping'
    name = 'apps.shipping'
    verbose_name = 'Shipping'
