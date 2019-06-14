import oscar.apps.dashboard.offers.apps as apps


class OffersDashboardConfig(apps.OffersDashboardConfig):
    label = 'offers_dashboard'
    name = 'apps.dashboard.offers'
    verbose_name = 'Offers dashboard'
