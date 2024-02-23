from django.urls import path

from . import views
from .views import detail, delete, edit, add

app_name = 'shop'


urlpatterns = [
    path('', views.search, name='search'),
    path('product/add/', views.add, name='add_product'),
    path('product/<int:pk>', views.detail, name='detail'),
    path('product/<int:pk>/delete/', views.delete, name='delete'),
    path('product/<int:pk>/edit/', views.edit, name='edit'),
    ]
