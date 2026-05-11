from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from sslcommerz_python.payment import SSLCSession
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from core.views import send_email
from .forms import BillingAddressForm, PaymentMethodForm
from .models import BillingAddress
from django.views.generic import TemplateView
from order.models import Cart, Order
from fruit_sell.settings import STORE_ID, STORE_PASS
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from fruit_sell.settings import current_datetime

# Create your views here.
@method_decorator(login_required, name='dispatch')
class CheckoutTemplateView(TemplateView):
    
    def get(self, request, *args, **kwargs):
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        order = None
        if carts.exists() and orders.exists():
            order = orders[0]
            
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_method = PaymentMethodForm()
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order_item = order_qs[0].order_items.all()
        order_total = order_qs[0].get_totals()

        context = {
            'carts':carts,
            'order':order,
            'billing_address':form,
            'payment_method':payment_method,
            'order_item':order_item,
            'order_total':order_total,
        }

        return render(request, 'checkout.html', context)
    
    def post(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_obj = Order.objects.filter(user=request.user, ordered=False)[0]
        payment_form = PaymentMethodForm(instance=payment_obj)
        if request.method == 'post' or request.method == 'POST':
            form = BillingAddressForm(request.POST, instance=saved_address)
            pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
            if form.is_valid() and pay_form.is_valid():
                form.save()
                pay_method = pay_form.save()
                
                if pay_method.payment_method == 'Cash on delivery':
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order = order_qs[0]
                    order.ordered = True
                    order.orderId = order.id
                    order.paymentId = pay_method.payment_method
                    order.timestamp = current_datetime
                    order.save()

                    cart_items = Cart.objects.filter(user=request.user, purchased=False)
                    for item in cart_items:
                        item.purchased = True
                        item.save()
                    messages.success(request,f'Your order successfully placed for delivery!')
                    send_email(request.user, request.user.email, "Order placed successfully", "order_mail.html")
                    return redirect('home')
                
                elif pay_method.payment_method == 'SSLCOMMERZ':
                    store_id = STORE_ID
                    store_pass = STORE_PASS

                    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=store_pass)


                    status_url = request.build_absolute_uri(reverse('status'))
                    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)
                    
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order_items = order_qs[0].order_items.all()
                    order_item_count = order_qs[0].order_items.count()
                    order_total = order_qs[0].get_totals()
                    
                    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='fruits', product_name=order_items, num_of_item=order_item_count, shipping_method='Courier', product_profile='None')

                    current_user = request.user
                    name = f'{current_user.first_name} {current_user.last_name}'
                    email = current_user.email
                    billing_address = BillingAddress.objects.filter(user=request.user)[0]
                    address = billing_address.address
                    district = billing_address.district
                    postal_code = billing_address.postal_code
                    phone = billing_address.phone_number

                    mypayment.set_customer_info(name=name, email=email, address1=address, city=district, postcode=postal_code, country='Bangladesh', phone=phone)

                    mypayment.set_shipping_info(shipping_to=name, address=address, city=district, postcode=postal_code, country='Bangladesh')

                    response_data = mypayment.init_payment()

                    return redirect(response_data['GatewayPageURL'])
        else:
            return redirect('home')

@csrf_exempt
def sslc_status(request):
    if request.method == 'post' or request.method == 'POST':
        payment_data = request.POST
        status = payment_data['status']
        if status == 'VALID':
            val_id = payment_data['val_id']
            tran_id = payment_data['tran_id']

            return HttpResponseRedirect(reverse('sslc_complete', kwargs={'val_id':val_id, 'tran_id': tran_id}))
        elif status == 'FAILED':
            messages.warning(request,f'Payment failed. Please try again.!')
            return redirect('home')
@login_required
def sslc_complete(request,val_id, tran_id):
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.orderId = order.id
    order.paymentId = tran_id
    order.timestamp = current_datetime
    print(current_datetime)
    order.save()
    cart_items = Cart.objects.filter(user=request.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    messages.success(request,f'You have purchased the order successfully. Your order placed for delivery!')
    send_email(request.user, request.user.email, "Order placed successfully", "order_mail.html")
    return redirect('home')