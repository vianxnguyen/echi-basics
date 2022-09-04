from djongo import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.
CATEGORY_CHOICES = (
    ('Pair', 'Pair'),
    ('Bundle', 'Bundle'),
)
class Customer(models.Model):
	 user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	 name = models.CharField(max_length=200, null=True, blank=True)
	 email = models.CharField(max_length=200, null=True, blank=True)
	device = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.device

class Item(models.Model):
    title = models.CharField(max_length=100)
    stock_quantity = models.IntegerField(default=0)
    price = models.FloatField()
    discounted_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    slug = models.SlugField()
    short_description = models.TextField(default="short test description")
    long_description = models.TextField(default="long test description")
    img1 = models.ImageField(null=True, blank=True, upload_to='static/img')
    img2 = models.ImageField(null=True, blank=True, upload_to='static/img')
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("web_app:product", kwargs={
            'slug': self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("web_app:add-to-cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_price(self):
        return self.quantity * self.item.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    items = models.ManyToManyField(OrderItem, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    shipping_info = models.ForeignKey('ShippingInfo', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_cost = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.customer.device

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_price()
        total += self.shipping_cost
        return total
    
    def get_total_cents(self):
        total = self.get_total()
        total *= 100
        return total

    def get_cart_quantity(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.quantity
        return total
        
class ShippingInfo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.CharField(max_length=100)
    address_first = models.CharField(max_length=100)
    address_second = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name
