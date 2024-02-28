from django.urls import path

from . import views
from .views import detail, delete, edit, add, CartView, AddToCartView, UpdateCartView, RemoveFromCartView, CheckoutView, \
    OrderConfirmationView, OrderConfirmationView2

app_name = 'shop'


urlpatterns = [
    path('', views.search, name='search'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:product_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('success/<int:order_id>', OrderConfirmationView.as_view(), name='order_success'),
    path('product/success/', OrderConfirmationView2.as_view(), name='order_success_no_id'),
    path('product/add/', views.add, name='add_product'),
    path('product/<int:pk>/', views.detail, name='detail'),
    path('product/<int:pk>/delete/', views.delete, name='delete'),
    path('product/<int:pk>/edit/', views.edit, name='edit'),
    ]
