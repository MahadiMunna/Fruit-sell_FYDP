from django.contrib import admin
from .models import FruitModel, Vendor, FavouriteFruit, Wishlist
# Register your models here.

admin.site.register(Vendor)
admin.site.register(FruitModel)
admin.site.register(FavouriteFruit)
admin.site.register(Wishlist)