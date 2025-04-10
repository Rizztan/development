from django.urls import path
from .views import HelloWorld, Students, ContactListView
from .exam_views import ChatView
from .store_views import ProductListView, CartView, OrderView, OrderConfirmationView

urlpatterns = [
    path('hello/', HelloWorld.as_view(), name='hello_world'),
    path('Students/', Students.as_view(), name='list_student'),
    path('contact/', ContactListView.as_view(), name='contact_new'),
    path('chat/', ChatView.as_view(), name='chat_view'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('orders/', OrderView.as_view(), name='order'),
    path('orders/confirm/', OrderConfirmationView.as_view(), name='order_confirm'),
]