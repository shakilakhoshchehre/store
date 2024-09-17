### python manage.py makemigrations
### ru
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


from django.db import models

def validate_phone(value):
    if not (11 <= len(str(value)) <= 14):
        raise ValidationError('Phone number must be between 11 and 14 digits.')

class ProductOwner(models.Model):
    name = models.CharField(max_length=100, default='Unknown')
    family = models.CharField(max_length=100, default='Unknown')
    phone = models.IntegerField()
    email = models.EmailField(null=True)

    def __str__(self):
        return f"{self.name} {self.family}"

class Category(models.Model):
    product_owner = models.ForeignKey(ProductOwner, on_delete=models.CASCADE, related_name='categories',default=1)
    name = models.CharField(max_length=100, default='Unknown')
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(default='default.jpg', upload_to='images/')

    def __str__(self):
        return self.name

class Product(models.Model):
    CHOICES = [
        ('small', 'small'),
        ('medium', 'medium'),
    ]
    COLOR_CHOICES = [
        ('red', 'red'),
        ('yellow', 'yellow'),
        ('blue', 'blue'),
    ]
    product_owner = models.ForeignKey(ProductOwner, on_delete=models.CASCADE, related_name='products', default=1)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, )
    amount = models.IntegerField()
    price = models.IntegerField()
    discount = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField(editable=False)
    size = models.CharField(max_length=50, choices=CHOICES)
    color = models.CharField(max_length=6, choices=COLOR_CHOICES)

    def calculate_total_price(self):
        if self.discount is None:
            return self.price
        discount_amount = (self.price * self.discount) / 100
        return self.price - discount_amount

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.size}, {self.color})"






class User(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    phone = models.IntegerField(validators=[validate_phone])
    family = models.CharField(max_length=100, default='Unknown')
    address = models.CharField(max_length=100, default='Unknown')
    email = models.EmailField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderProduct')

    def __str__(self):
        return f"Order by {self.user.user_name} on {self.date}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        return self.amount * self.product.total_price

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super(OrderProduct, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order.id} - Product {self.product.name} - Amount {self.amount}"














