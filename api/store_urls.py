from django.urls import path
from .store_views import ProductListView, CartView, OrderView, OrderConfirmationView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderView.as_view(), name='order'),
    path('orders/confirm/', OrderConfirmationView.as_view(), name='order_confirm'),
]