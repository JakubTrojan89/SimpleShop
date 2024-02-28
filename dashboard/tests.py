import pytest
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.urls import reverse

from dashboard.views import index
from shop.models import Product


@pytest.mark.django_db
def test_index_view():
    # Create a user
    user = User.objects.create_user(username='test_user', password='password123')

    # Create some products associated with the user
    product1 = Product.objects.create(name='Product 1', price=10, created_by=user)
    product2 = Product.objects.create(name='Product 2', price=2, created_by=user)

    # Create a mock request object
    request = HttpRequest()
    request.user = user
    request.method = 'GET'
    request.path = reverse('index')  # Assuming the URL name is 'index'

    # Call the view function
    response = index(request)

    # Check if the response is successful (HTTP 200)
    assert response.status_code == 200

    # Check if the products are passed to the template context
    assert 'products' in response.context

    # Check if the products passed to the template context are the same as the products created
    assert list(response.context['products']) == [product1, product2]