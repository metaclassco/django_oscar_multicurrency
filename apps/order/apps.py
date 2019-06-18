import oscar.apps.order.apps as apps


class OrderConfig(apps.OrderConfig):
    label = 'order'
    name = 'apps.order'
    verbose_name = 'Order'
