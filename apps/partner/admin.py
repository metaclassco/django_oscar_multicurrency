from django.contrib import admin
from .models import Currency


admin.site.register(Currency)


from oscar.apps.partner.admin import *  # noqa
