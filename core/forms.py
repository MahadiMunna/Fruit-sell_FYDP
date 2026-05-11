from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Write your full Name ",required=True,  widget = forms.TextInput(attrs={'class': 'form-control', 'id':'text-area', 'placeholder':'Enter your full name'}))
    email = forms.EmailField(label="Write your email",required=False, widget = forms.TextInput(attrs={'class': 'form-control', 'id':'text-area', 'placeholder':'Enter your email'}))
    feedback = forms.CharField(label="Write your feedback ",required=True, widget = forms.Textarea(attrs={'class': 'form-control', 'id':'text-area', 'placeholder':'Write your feedback'}))

         