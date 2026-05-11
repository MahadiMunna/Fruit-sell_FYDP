from django.shortcuts import render, redirect
from fruit.models import FruitModel
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from .forms import ContactForm

# Create your views here.
def home(request):
    data = FruitModel.objects.filter(flash_sale=False).order_by("?")
    flashsale = FruitModel.objects.filter(flash_sale=True)
    return render(request, 'home.html', {'data':data, 'flashsale':flashsale })

def send_email(user, email_to, subject, template):
        message = render_to_string(template, {
            'user' : user,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[email_to])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

def send_contact_email(name, email, feedback):
        message = render_to_string("contact_mail.html", {
            'name' : name,
            'email' : email,
            'feedback' : feedback,
        })
        send_email = EmailMultiAlternatives('Feedback mail from Fruitchain', '', to=["mahadimunna.official@gmail.com"])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            feedback = form.cleaned_data['feedback']
            send_contact_email(name, email, feedback)
            messages.success(request,'Your message successfully send! Thank you for contacting us.')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact.html',{'form':form})