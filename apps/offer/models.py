from django.db import models

from oscar.apps.offer.abstract_models import AbstractBenefit
from oscar.core.utils import get_default_currency


class Benefit(AbstractBenefit):
    currency = models.CharField(max_length=3, default=get_default_currency)


from oscar.apps.offer.models import *  # noqa isort:skip
