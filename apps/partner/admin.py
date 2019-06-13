from django.contrib import admin
from .models import ExchangeRate


class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('base_currency', 'currency', 'value', 'date_created')


admin.site.register(ExchangeRate, ExchangeRateAdmin)


from oscar.apps.partner.admin import *  # noqa
