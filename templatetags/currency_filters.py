from decimal import Decimal as D
from decimal import InvalidOperation

from babel.numbers import format_currency
from django import template
from django.conf import settings
from django.utils.translation import get_language, to_locale

from apps.partner.utils import get_default_currency

register = template.Library()


@register.filter(name='currency')
def currency(value, currency=None):
    try:
        value = D(value)
    except (TypeError, InvalidOperation):
        return ""

    OSCAR_CURRENCY_FORMAT = getattr(settings, 'OSCAR_CURRENCY_FORMAT', None)

    # Fallback to default currency, if it's not provided.
    # Although, unlike original Oscar implementation, we don't use
    # OSCAR_DEFAULT_CURRENCY setting, but determine it in the function.
    if not currency:
        currency = get_default_currency()
    kwargs = {
        'currency': currency.code, 'locale': to_locale(get_language() or settings.LANGUAGE_CODE)
    }
    if isinstance(OSCAR_CURRENCY_FORMAT, dict):
        kwargs.update(OSCAR_CURRENCY_FORMAT.get(currency, {}))
    else:
        kwargs['format'] = OSCAR_CURRENCY_FORMAT
    return format_currency(value, **kwargs)
