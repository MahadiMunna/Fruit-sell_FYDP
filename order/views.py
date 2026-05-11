from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from core.views import send_email
from fruit.models import FruitModel
from order.forms import OrderForm
from .models import Cart, Order
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from fruit_sell.settings import current_datetime
from datetime import timedelta
from .forms import OrderForm
import openpyxl


# Create your views here.
@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(FruitModel, pk=pk)
    order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    view_cart = reverse('cart')
    if order_qs.exists():
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.success(request,f'{item.name} added to your cart! <a class="text-decoration-none" href="{view_cart}">Go to cart!</a>')
            referer_url = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer_url)
        else:
            order.order_items.add(order_item[0])
            messages.success(request,f'{item.name} added to your cart! <a class="text-decoration-none" href="{view_cart}">Go to cart!</a>')
            referer_url = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer_url)
    else:
        order = Order(user=request.user)
        order.save()
        order.order_items.add(order_item[0])
        messages.success(request,f'{item.name} added to your cart! <a class="text-decoration-none" href="{view_cart}">Go to cart!</a>')
        referer_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(referer_url)

@login_required
def cart_view(request):
    data = FruitModel.objects.all().order_by("?")
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        context = {
            'carts':carts,
            'order':order,
            'data':data,
        }
        return render(request, 'cart.html', context)
    else:
        data = FruitModel.objects.all()
        context = {
            'data':data,
        }
        return render(request, 'cart.html', context)

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(FruitModel, pk=pk)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if orders.exists():
        order = orders[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.order_items.remove(order_item)
            order_item.delete()
            messages.warning(request,f'{item.name} removed from cart!')
            referer_url = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer_url)
        else:
            referer_url = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer_url)
    else:
        referer_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(referer_url)

@login_required
def increase_decrease(request, pk, type):
    item = get_object_or_404(FruitModel, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if type=='increase':
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    referer_url = request.META.get('HTTP_REFERER', '/')
                    return HttpResponseRedirect(referer_url)
            elif type=='decrease':
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    referer_url = request.META.get('HTTP_REFERER', '/')
                    return HttpResponseRedirect(referer_url)
                else:
                    order.order_items.remove(order_item)
                    order_item.delete()
                    messages.warning(request,f'{item.name} removed from cart!')
                    referer_url = request.META.get('HTTP_REFERER', '/')
                    return HttpResponseRedirect(referer_url)
        else:
            referer_url = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer_url)
    else:
        referer_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(referer_url)

@login_required    
def remove_order(request, id):
    order = Order.objects.filter(id=id, user=request.user)
    order.delete()
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)

@login_required    
def cancel_order(request, id):
    order = Order.objects.filter(id=id, user=request.user)[0]
    order.cancelled = True
    order.order_status = 'Cancelled'
    order.save()
    messages.warning(request, 'Your order has been cancelled!')
    send_email(request.user, request.user.email, "Order cancelled!", "cancel_mail.html")
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)

class OrdersView(TemplateView):
    template_name = 'orders.html'
    def get(self, request):
         yesterday = current_datetime - timedelta(days=1)
         orders = Order.objects.filter(ordered=True).order_by('-timestamp')
         return render(request, self.template_name, {'orders': orders, 'current_datetime':current_datetime, 'yesterday':yesterday})

class UpdateOrdersView(TemplateView):
    template_name = 'update_orders.html'
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
         yesterday = current_datetime - timedelta(days=1)
         order_id = kwargs.get(self.pk_url_kwarg)
         order_instance =  get_object_or_404(Order, id=order_id)
         form = OrderForm(instance=order_instance)
         orders = Order.objects.filter(ordered=True).order_by('-timestamp')
         return render(request, self.template_name, {'form':form, 'orders': orders, 'order_instance':order_instance,'current_datetime':current_datetime, 'yesterday':yesterday})

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get(self.pk_url_kwarg)
        order_instance =  get_object_or_404(Order, id=order_id)
        form = OrderForm(request.POST, request.FILES, instance=order_instance)
        if form.is_valid():
            if form.cleaned_data.get('order_status') == 'Cancelled':
                order_instance.cancelled = True
                order_instance.save()
            form.save()
            messages.success(self.request, 'Order status updated successfully!')
            return redirect('orders')
        return render(request, self.template_name, {'form': form})

def export_orders_to_excel(request):
    orders = Order.objects.filter(ordered=True).order_by('-timestamp')

    # Create a new workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orders"

    # Define the columns and write the header
    columns = ["Order Id", "Customer", "Date & Time", "Ordered Items", "Total Cost", "Payment Method", "Order Status"]
    ws.append(columns)

    # Write data to the worksheet
    for order in orders:
        items = ", ".join([f"{item.item.name} x {item.quantity}(kg)" for item in order.order_items.all()])
        ws.append([
            order.orderId,
            f"{order.user.first_name} {order.user.last_name}",
            order.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            items,
            f"{order.get_totals()}৳",
            order.payment_method,
            order.order_status
        ])

    # Set the response content type and headers
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="orders.xlsx"'

    # Save the workbook to the response
    wb.save(response)
    return response


@login_required
def remove_order_by_admin(request, id):
    Order.objects.filter(id=id)[0].delete()
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)