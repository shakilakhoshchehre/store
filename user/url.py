# urls.py
from django.urls import path
from .views import ProductListView, CategoryWithProductsListView, SearchProductOwnerNameView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('categories-with-products/', CategoryWithProductsListView.as_view(), name='category-with-products-list'),
    path('search-productowner-name/', SearchProductOwnerNameView.as_view(), name='search-product-owner-name'),
]
