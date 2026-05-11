from django.contrib import admin
from .models import FruitModel, Vendor,  Wishlist, Comment
# Register your models here.

admin.site.register(Vendor)
admin.site.register(FruitModel)
admin.site.register(Wishlist)
admin.site.register(Comment)