import oscar.apps.dashboard.apps as apps


class DashboardConfig(apps.DashboardConfig):
    label = 'dashboard'
    name = 'apps.dashboard'
    verbose_name = 'Dashboard'
