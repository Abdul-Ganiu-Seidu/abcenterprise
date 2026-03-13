from django.contrib import admin
from .models import PrintOrder, PrintPricing

@admin.register(PrintPricing)
class PrintPricingAdmin(admin.ModelAdmin):
    list_display = ('text_bw_price', 'text_color_price', 'photo_bw_price', 'photo_color_price', 'delivery_fee')

@admin.register(PrintOrder)
class PrintOrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone', 'print_type', 'color_type', 'copies', 'pages', 'delivery_method', 'price', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'delivery_method', 'color_type', 'print_type')
    search_fields = ('customer_name', 'phone')