from django import forms
from .models import PrintOrder, PrintPricing

class PrintOrderForm(forms.ModelForm):
    class Meta:
        model = PrintOrder
        fields = [
            'customer_name',
            'phone',
            'document',
            'print_type',
            'copies',
            'pages',
            'color_type',
            'delivery_method',
            'delivery_address',
            'payment_method'
        ]
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows':3}),
        }