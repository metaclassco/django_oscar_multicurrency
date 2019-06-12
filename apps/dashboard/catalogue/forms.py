from oscar.apps.dashboard.catalogue import forms


class StockRecordForm(forms.StockRecordForm):
    class Meta:
        fields = [
            'partner', 'partner_sku', 'currency', 'price_excl_tax', 'price_retail',
            'cost_price', 'num_in_stock', 'low_stock_threshold',
        ]
