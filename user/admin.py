
# Register your models here.
from django.contrib import admin
from .models import *

@admin.register(ProductOwner)
class ProductOwnerAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'name', 'family', 'phone', 'email')
    search_fields = ('name', 'family', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_owner', 'name', 'slug', 'image')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_owner', 'category', 'name', 'amount','price','discount','total_price','size','color')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'phone', 'family', 'address','email','date')
    search_fields = ('user_name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date')
    search_fields = ('user',)

@admin.register(OrderProduct)
class Order_productAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'amount', 'total_price','date')
    search_fields = ('order',)