from .forms import BasketCurrencyForm


def currency_form(request):
    """
    Context processor container currency selection form, which
    should be available throughout all site pages.
    """
    return {'currency_form': BasketCurrencyForm(request.GET)}
