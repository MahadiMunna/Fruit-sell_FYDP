from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import DetailView
from fruit.models import FruitModel, Vendor, Wishlist, Comment
from django.contrib import messages
from .forms import FruitForm, VendorForm, CommentForm
from order.models import Order
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from blockchain import get_fruit
from django.core.paginator import Paginator

# Create your views here.
def available_fruits(request):
    p = Paginator(FruitModel.objects.filter(stocked_out=False),9)
    page = request.GET.get('page')
    data = p.get_page(page)
    return render(request, 'fruits.html', {'data':data })

class DetailFruitView(DetailView):
    model = FruitModel
    pk_url_kwarg = 'id'
    template_name = 'fruit_details.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return self.get(request, *args, **kwargs)
         
        comment_form = CommentForm(request.POST, request.FILES)
        post = self.get_object()
        user_account = request.user.account

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.name = user_account
            comment.post = post
            comment.save()
            messages.success(request, 'Thank you for your review!')
        else:
            messages.warning(request, 'Error! Review not saved.')
            print(comment_form.errors)  # For debugging

        referer_url = request.META.get('HTTP_REFERER', '/')
        return HttpResponseRedirect(referer_url)

    def reviewer(self, user, fruit):
        if not user.is_authenticated:
            return False
        delivered_orders = Order.objects.filter(user=user, order_status='Delivered', ordered=True)
        for order in delivered_orders:
            if order.order_items.filter(item=fruit).exists():
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = self.object
        comments = post.comments.all().order_by('-created_on')
        comment_form = CommentForm()
        can_review = self.reviewer(user, post)
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['can_review'] = can_review
        if post.blockchain_id:
            try:
                blockchain_data = get_fruit(post.id)
                # Add debugging prints
                # print(f"Blockchain data for fruit ID {post.id}: {blockchain_data}")
                context['blockchain_data'] = blockchain_data
            except Exception as e:
                print(f"Error fetching blockchain data: {e}")
                context['blockchain_data'] = None
        return context

@login_required
def add_fruit(request):
    if request.method == 'POST':
        fruit_form = FruitForm(request.POST, request.FILES)

        if fruit_form.is_valid():
            name = fruit_form.cleaned_data.get("name")
            image = fruit_form.cleaned_data.get("image")
            description = fruit_form.cleaned_data.get("description")
            location = fruit_form.cleaned_data.get("location")
            vendor = fruit_form.cleaned_data.get("vendor")
            supply_date = fruit_form.cleaned_data.get("supply_date")
            expiry_date = fruit_form.cleaned_data.get("expiry_date")
            unit = fruit_form.cleaned_data.get("unit")
            price = fruit_form.cleaned_data.get("price")
            discount = fruit_form.cleaned_data.get("discount")
            new_fruit = FruitModel.objects.create(
                name=name,
                description=description,
                location=location,
                supply_date=supply_date,
                expiry_date=expiry_date,
                unit=unit,
                price=price,
                image=image,
                vendor=vendor,
                discount=discount
            )
            try:
                new_fruit.save_to_blockchain()
                messages.success(request, 'New fruit added and saved to blockchain successfully!')
            except Exception as e:
                messages.warning(request, f"Error adding fruit to blockchain: {e}")
            # messages.success(request, 'New fruit added successfully!')
            return redirect('fruits')
    else:
        fruit_form = FruitForm()

        return render(request, 'add_fruit.html', {'form': fruit_form})
    return render(request, 'add_fruit.html', {'form': fruit_form})

@method_decorator(login_required, name='dispatch')
class EditFruitView(View):
    template_name = 'edit_fruit.html'
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        fruit_id = kwargs.get(self.pk_url_kwarg)
        fruit_instance = get_object_or_404(FruitModel, id=fruit_id)
        form = FruitForm(instance=fruit_instance)
        return render(request, self.template_name, {'form': form, 'fruit_instance': fruit_instance})

    def post(self, request, *args, **kwargs):
        fruit_id = kwargs.get(self.pk_url_kwarg)
        fruit_instance = get_object_or_404(FruitModel, id=fruit_id)
        blockchain_id = fruit_instance.blockchain_id
        form = FruitForm(request.POST, request.FILES, instance=fruit_instance)
        if form.is_valid():
            fruit_instance = form.save(commit=False)
            fruit_instance.blockchain_id = blockchain_id
            fruit_instance.save()
            messages.success(self.request, 'Fruit post updated successfully!')
            referer_url = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(referer_url)
        return render(request, self.template_name, {'form': form})

@login_required
def add_vendor(request):
    vendor_form = VendorForm()
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST, request.FILES)
        if vendor_form.is_valid():
            vendor_name = vendor_form.cleaned_data.get("vendor_name")
            NID_number = vendor_form.cleaned_data.get("NID_number")
            phone_number = vendor_form.cleaned_data.get("phone_number")
            address = vendor_form.cleaned_data.get("address")

            Vendor.objects.create(
                vendor_name=vendor_name,
                NID_number=NID_number,
                phone_number=phone_number,
                address=address,
            )
            messages.success(request, 'New vendor added successfully. Add more vendor!')
            return redirect('add_vendor')
        else:
            return render(request, 'add_vendor.html', {'form': vendor_form })
    return render(request, 'add_vendor.html', {'form': vendor_form })

@login_required
def make_stocked_out(request, id):
    fruit = get_object_or_404(FruitModel, id=id)
    fruit.stocked_out = True
    fruit.flash_sale = False
    fruit.save()
    messages.success(request, f'{fruit.name} marked as stocked out!')
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)

@login_required
def archive_fruits(request):
    data = FruitModel.objects.filter(stocked_out=True)
    return render(request, 'archive_fruits.html', {'data':data})

@login_required
def move_to_regular(request, id):
    fruit = get_object_or_404(FruitModel, id=id)
    fruit.stocked_out = False
    fruit.save()
    messages.success(request, f'{fruit.name} added in stocks!')
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)

@login_required
def remove_fruit(request, id):
    fruit = get_object_or_404(FruitModel, id=id)
    messages.success(request, f'{fruit.name} removed successfully!')
    fruit.delete()
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)

@login_required
def add_to_flash_sale(request, id):
    fruit = get_object_or_404(FruitModel, id=id)
    fruit.flash_sale = True
    fruit.save()
    messages.success(request, f'{fruit.name} added to flash sale!')
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)

@login_required
def flash_sale_fruits(request):
    data = FruitModel.objects.filter(flash_sale=True)
    return render(request, 'flash_sale.html', {'data':data})

@login_required
def make_regular_sale(request, id):
    fruit = get_object_or_404(FruitModel, id=id)
    fruit.flash_sale = False
    fruit.save()
    messages.success(request, f'{fruit.name} moved to regular sale!')
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)


@login_required
def add_to_wishlist(request, id):
    fruit = get_object_or_404(FruitModel, id=id)
    Wishlist.objects.get_or_create(user=request.user, fruit=fruit)
    messages.success(request, f'{fruit.name} added to wishlist successfully!')
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)

@login_required
def wishlist(request):
    fruits = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'fruits': fruits})

@login_required
def remove_from_wishlist(request, id):
    wish_fruit = get_object_or_404(Wishlist, id=id, user=request.user)
    messages.success(request, f'{wish_fruit.fruit.name} removed from wishlist successfully!')
    wish_fruit.delete()
    referer_url = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(referer_url)