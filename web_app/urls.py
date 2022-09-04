from web_app.models import Item
from django.urls import path
from .views import (
    HomeView, 
    ShopView,
    ItemDetailView,
    CartView,
    PaymentView,
    add_to_cart,
    remove_from_cart,
    remove_single_from_cart,
    success
)

app_name = 'web_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/<slug>',ItemDetailView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', remove_from_cart, name='remove-from-cart'),
    path('remove-single-from-cart/<slug>', remove_single_from_cart, name='remove-single-from-cart'),
    path('payment-session/', PaymentView.as_view(), name='payment-session'),
    path('success/', success, name='success')
]
