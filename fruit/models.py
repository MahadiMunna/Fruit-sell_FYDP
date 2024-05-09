from django.db import models
from django.contrib.auth.models import User
from users.models import UserAccount

# Create your models here.
class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100)
    NID_number = models.CharField(max_length=17)
    phone_number = models.CharField(max_length=14)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.vendor_name}"
class FruitModel(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='./fruit-images/', blank=True, null=True)
    description=models.TextField()
    location=models.CharField(max_length=100)
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    supply_date=models.DateField()
    price=models.DecimalField(max_digits=8, decimal_places=2)
    discount=models.DecimalField(max_digits=8, decimal_places=2,default=0)
    timestamp=models.DateTimeField(auto_now=True)
    stocked_out = models.BooleanField(default=False)
    flash_sale = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name} from {self.location}"
    
    def get_discounted_price(self):
        if self.discount > 0:
            discount_amount = (self.price * self.discount) / 100
            discounted_price = self.price - discount_amount
            return format(discounted_price, "0.2f")
        else:
            return self.price

class FavouriteFruit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fruit = models.ForeignKey(FruitModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.fruit.name}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fruit = models.ForeignKey(FruitModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} looking for: {self.fruit.name}"
   
class Comment(models.Model):
    post = models.ForeignKey(FruitModel, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comments by {self.name}"