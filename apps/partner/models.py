from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.name


from oscar.apps.partner.models import *  # noqa isort:skip
