import oscar.apps.partner.apps as apps


class PartnerConfig(apps.PartnerConfig):
    label = 'partner'
    name = 'apps.partner'
    verbose_name = 'Partner'
