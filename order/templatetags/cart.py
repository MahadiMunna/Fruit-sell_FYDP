from django import template
from order.models import Cart, Order

register = template.Library()

@register.filter
def cart_view(user):
    cart = Cart.objects.filter(user=user, purchased=False)
    if cart.exists():
        return cart
    else:
        return cart

@register.filter
def cart_total(user):
    order = order.objects.filter(user=user, ordered=False)
    if order.exists():
        return order[0].get_totals()
    else:
        return 0