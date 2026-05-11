from django import forms
from .models import BillingAddress
from order.models import Order

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = '__all__'

        widgets = {
          'address': forms.Textarea(attrs={'rows':3}),
        }
    def __init__(self, *args, **kwargs):
        super(BillingAddressForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
          self.fields[field_name].required = True
        
        self.fields['user'].label = "User name"
        self.fields['user'].disabled = True
        self.fields['user'].required = False 

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['payment_method',]