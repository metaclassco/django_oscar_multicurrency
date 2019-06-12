import oscar.apps.dashboard.catalogue.apps as apps


class CatalogueDashboardConfig(apps.CatalogueDashboardConfig):
    label = 'catalogue_dashboard'
    name = 'apps.dashboard.catalogue'
    verbose_name = 'Catalog'
