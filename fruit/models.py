from django.db import models
from django.contrib.auth.models import User
from users.models import UserAccount
from blockchain import add_fruit

# Create your models here.
class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100)
    NID_number = models.CharField(max_length=17)
    phone_number = models.CharField(max_length=14)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.vendor_name}"
class FruitModel(models.Model):
    blockchain_id = models.CharField(max_length=100, blank=True, null=True)
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='./fruit-images/', blank=True, null=True)
    description=models.TextField()
    location=models.CharField(max_length=100)
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=True, null=True)
    supply_date=models.DateField(blank=True, null=True)
    expiry_date=models.DateField(blank=True, null=True)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    unit=models.CharField(max_length=100, blank=True, null=True)
    discount=models.DecimalField(max_digits=8, decimal_places=2,default=0)
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
        
    def save_to_blockchain(self):
        try:
            receipt = add_fruit(
                self.name,
                self.location,
                str(self.supply_date),
                str(self.expiry_date),
                self.vendor.vendor_name,
                self.description,  # Assuming description is used as trace_info
                self.id
            )
            self.blockchain_id = receipt['transactionHash'].hex()
            self.save()
            # print(f"Blockchain ID saved: {self.blockchain_id}")
        except Exception as e:
            print(f"Error saving to blockchain: {e}")
            raise

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fruit = models.ForeignKey(FruitModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} looking for: {self.fruit.name}"
   
class Comment(models.Model):
    post = models.ForeignKey(FruitModel, on_delete=models.CASCADE, related_name='comments')
    name = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    review = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='./review-images/uploads/', blank=True, null=True)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return f"Review by {self.name}"