from rest_framework import serializers
from .models import *

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOwner
        fields = '__all__'


class ProductOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOwner
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount', 'total_price', 'size', 'color']

class CategoryWithProductsSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_owner = ProductOwnerSerializer(read_only=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count',  'products']


    def get_product_count(self, obj):
        return obj.products.count()
