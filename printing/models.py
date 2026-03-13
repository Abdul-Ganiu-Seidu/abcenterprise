from django.db import models

class PrintPricing(models.Model):
    text_bw_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.50, verbose_name="Text B/W Price per Page")
    text_color_price = models.DecimalField(max_digits=6, decimal_places=2, default=1.50, verbose_name="Text Color Price per Page")
    photo_bw_price = models.DecimalField(max_digits=6, decimal_places=2, default=1.00, verbose_name="Photo B/W Price per Page")
    photo_color_price = models.DecimalField(max_digits=6, decimal_places=2, default=2.00, verbose_name="Photo Color Price per Page")
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=5.00, verbose_name="Home Delivery Fee")

    def __str__(self):
        return "Current Print Pricing"

    class Meta:
        verbose_name_plural = "Print Pricing"


class PrintOrder(models.Model):

    COLOR_CHOICES = [
        ('bw', 'Black & White'),
        ('color', 'Color'),
    ]

    PRINT_TYPE = [
        ('text', 'Text Document'),
        ('photo', 'Photo Print'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('printing', 'Printing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
    ]

    DELIVERY_CHOICES = [
        ('pickup', 'Pickup at Shop'),
        ('delivery', 'Home Delivery'),
    ]

    PAYMENT_METHOD = [
        ('momo', 'Mobile Money'),
        ('card', 'Card Payment'),
    ]

    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    document = models.FileField(upload_to='print_orders/')

    print_type = models.CharField(max_length=10, choices=PRINT_TYPE)
    copies = models.IntegerField(default=1)
    pages = models.IntegerField()
    color_type = models.CharField(max_length=10, choices=COLOR_CHOICES)

    # DELIVERY
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='pickup')
    delivery_address = models.TextField(blank=True, null=True)

    # PAYMENT
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='unpaid')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from .models import PrintPricing

        pricing = PrintPricing.objects.first()
        if not pricing:
            pricing = PrintPricing.objects.create()  # fallback default prices

        # Determine price per page
        if self.print_type == 'text' and self.color_type == 'bw':
            price_per_page = pricing.text_bw_price
        elif self.print_type == 'text' and self.color_type == 'color':
            price_per_page = pricing.text_color_price
        elif self.print_type == 'photo' and self.color_type == 'bw':
            price_per_page = pricing.photo_bw_price
        else:
            price_per_page = pricing.photo_color_price

        total = price_per_page * self.pages * self.copies

        # Add delivery fee if applicable
        if self.delivery_method == 'delivery':
            total += pricing.delivery_fee

        self.price = total
        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer_name