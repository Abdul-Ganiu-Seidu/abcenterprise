from django.shortcuts import render, redirect
from .forms import PrintOrderForm
from .models import PrintOrder, PrintPricing

def printing_page(request):
    return render(request, 'printing/printing.html')


def upload_print(request):
    # Get pricing from admin-configurable model
    pricing = PrintPricing.objects.first()
    if not pricing:
        # Create default pricing if none exists
        pricing = PrintPricing.objects.create(
            text_bw_price=0.50,
            text_color_price=1.50,
            photo_bw_price=1.00,
            photo_color_price=2.00,
            delivery_fee=5.00
        )

    if request.method == 'POST':
        form = PrintOrderForm(request.POST, request.FILES)
        if form.is_valid():
            # Save instance without committing to calculate price & payment
            order = form.save(commit=False)

            # Calculate price based on print type, color, pages, copies
            if order.print_type == 'photo' and order.color_type == 'bw':
                price_per_page = pricing.photo_bw_price
            elif order.print_type == 'photo' and order.color_type == 'color':
                price_per_page = pricing.photo_color_price
            elif order.print_type == 'text' and order.color_type == 'bw':
                price_per_page = pricing.text_bw_price
            else:
                price_per_page = pricing.text_color_price

            total_price = price_per_page * order.pages * order.copies

            # Add delivery fee if home delivery is selected
            if order.delivery_method == 'delivery':
                total_price += pricing.delivery_fee

            order.price = total_price

            # Process payment (simulate here, integrate real gateway later)
            if order.payment_method:
                # Example: mark as paid and generate dummy transaction ID
                order.payment_status = 'paid'
                order.transaction_id = 'TXN' + str(order.id or 0).zfill(6)
            else:
                order.payment_status = 'unpaid'

            # Save the order with updated price & payment info
            order.save()
            # instead of return redirect('printing')
            return render(request, 'printing/payment_processing.html', {'order': order})
            # Optional: You can redirect to a success page or show receipt
            
    else:
        form = PrintOrderForm()

    return render(request, 'printing/upload.html', {
        'form': form,
        'pricing': pricing  # Pass pricing for dynamic JS price calculation
    })