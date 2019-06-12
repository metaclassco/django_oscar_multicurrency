from .forms import BasketCurrencyForm


def currency_form(request):
    return {'currency_form': BasketCurrencyForm(request.GET)}
