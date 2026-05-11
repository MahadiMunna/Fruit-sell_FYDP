from django import forms
from .models import Order
from django.forms import modelformset_factory

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status']

OrderFormSet = modelformset_factory(Order, form=OrderForm, extra=0)
