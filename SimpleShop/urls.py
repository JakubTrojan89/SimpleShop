from django.contrib import admin
from django.urls import path, include

from shop.views import index, contact, detail, add, delete, edit

urlpatterns = [
    path('', index, name='index'),
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('contact/', contact, name='contact'),
    path('product/', include('shop.urls')),
    path('dashboard/', include('dashboard.urls')),
]
