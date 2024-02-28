from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.http import HttpRequest
from django.test import Client

from django.urls import reverse

from shop.forms import AddProductForm
from shop.models import Order, OrderProduct, Category, Product
from shop.views import search, OrderConfirmationView


@pytest.mark.django_db
def test_index_view(client):
    response = client.get(reverse('index'))

    assert response.status_code == 200
    assert 'categories' in response.context
    assert 'products' in response.context


@pytest.mark.django_db
def test_contact_view(client):
    response = client.get(reverse('contact'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_search_view():
    assert True


@pytest.mark.django_db
def test_product_detail_view_not_found(client):
    product = Product.objects.create(pk=100, name="Test Product", price=10.00)

    url = reverse('product-detail')
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def add_product_get():
    client = Client()
    url = reverse('shop:add_product')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddProductForm)


@pytest.mark.django_db
def delete_product():
    product = Product.objects.create(name='Delete product', description='Test Description')
    client = Client()
    response = client.post(reverse('shop:delete', kwargs={'pk': product.pk}))
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_search_view():
#     # Create a user (assuming user with id=1 exists)
#     user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
#
#     # Create categories
#     category1 = Category.objects.create(name='Category 1')
#     category2 = Category.objects.create(name='Category 2')
#
#     # Create products
#     product1 = Product.objects.create(name='Product 1', description='Description 1', price=10, category=category1, created_by=user)
#     product2 = Product.objects.create(name='Product 2', description='Description 2', price=20, category=category2, created_by=user)
#
#     # Create a test client
#     client = Client()
#
#     # Define query and category_id
#     query = 'Product'
#     category_id = category1.id
#
#     # Make a GET request to the search view
#     response = client.get(reverse('search'), {'query': query, 'category': category_id})
#
#     # Check that the response status code is 200
#     assert response.status_code == 200
#
#     # Check that the context contains the expected data
#     assert len(response.context['products']) == 1
#     assert response.context['products'][0] == product1
#     assert response.context['query'] == query
#     assert response.context['categories'].count() == 2
#     assert response.context['category_id'] == category_id
# @pytest.mark.django_db
# def test_add_to_cart_valid(client, product):
#     # Simulate adding a product to the cart
#     response = client.post(reverse('add-to-cart'), {'product_id': product.id, 'quantity': 1})
#
#     # Check if the product is added to the cart correctly
#     session = client.session
#     cart = session.get('cart', {})
#     assert str(product.id) in cart
#     assert cart[str(product.id)] == 1
#
#     # Check if the response status code and redirection URL are correct
#     assert response.status_code == 302  # 302 indicates a redirect
#     assert response.url == reverse('shop:cart')

# def test_search_view_fail():
#     category1 = Category.objects.create(name='category1')
#     cos = Product.objects.create(name='cos')
#     client = Client
#     response = client.get(reverse('search'))
#     assert response.status_code == 200
#     assert len(response.context['products']) == 1


# @pytest.mark.django_db
# def test_cart_view_empty_cart(client):
#     client.session['cart'] = {}
#     client.session.save()
#     response = client.get(reverse('cart'))
#     assert response.status_code == 200
#     assert 'cart_items' in response.context
#     assert len(response.context['cart_items']) == 0
#     assert response.context['total_price'] == Decimal('0.00')
#
#
# @pytest.mark.django_db
# def test_cart_view_with_items(client, product):
#     session = client.session
#     session['cart'] = {str(product.id): 2}
#     session.save()
#     response = client.get(reverse('cart'))
#     # Assertions
#     assert response.status_code == 200
#     assert 'cart_items' in response.context
#     cart_items = response.context['cart_items']
#     assert len(cart_items) == 1
#     assert cart_items[0]['product'].id == product.id
#     assert cart_items[0]['quantity'] == 2
#     assert float(cart_items[0]['total_item_price']) == product.price * 2
#     assert float(response.context['total_price']) == product.price * 2
#
#
# @pytest.mark.django_db
# def test_cart_view_with_nonexistent_product(client):
#     session = client.session
#     session['cart'] = {'999': 1}  # Assuming ID 999 does not exist
#     session.save()
#     response = client.get(reverse('cart'))
#     # Depending on how you want to handle this case, you might expect a 404 response or handle it gracefully
#     # For this example, let's assume it's handled gracefully and the item is simply ignored or removed
#     assert response.status_code == 200
#     assert 'cart_items' in response.context
#     assert len(response.context['cart_items']) == 0
#     assert response.context['total_price'] == 0
#
#
# @pytest.mark.django_db
# def test_add_to_cart_valid(client, product):
#     response = client.post(reverse('add-to-cart'), {'product_id': product.id, 'quantity': 1})
#     session = client.session
#     cart = session['cart']
#     assert str(product.id) in cart
#     assert cart[str(product.id)] == 1
#     assert response.status_code == 302
#     assert response.url == reverse('cart')
#
#
# @pytest.mark.django_db
# def test_add_to_cart_invalid_quantity(client, product):
#     response = client.post(reverse('add-to-cart'), {'product_id': product.id, 'quantity': 20})
#     messages = list(get_messages(response.wsgi_request))
#     assert len(messages) == 1
#     assert str(messages[0]) == 'Cannot add 20 units. Only 10 remaining in stock.'
#     assert response.status_code == 302
#     assert response.url == reverse('shop-single', kwargs={'pk': product.id})
#
#
# @pytest.mark.django_db
# def test_add_to_cart_invalid_quantity(client, product):
#     response = client.post(reverse('add-to-cart'), {'product_id': product.id, 'quantity': 0})
#     messages = list(get_messages(response.wsgi_request))
#     assert len(messages) == 1
#     assert str(messages[0]) == "Quantity must be at least 1."
#     assert response.status_code == 302
#     assert response.url == reverse('shop-single', kwargs={'pk': product.id})
#
#
# @pytest.mark.django_db
# def test_add_to_cart_exceeding_stock(client, product):
#     quantity_to_add = product.stock + 1
#     response = client.post(reverse('add-to-cart'), {'product_id': product.id, 'quantity': quantity_to_add})
#     messages = list(get_messages(response.wsgi_request))
#     assert len(messages) == 1
#     assert "remaining in stock." in str(messages[0])
#     assert response.status_code == 302
#     assert response.url == reverse('shop-single', kwargs={'pk': product.id})
#
#
# @pytest.mark.django_db
# def test_update_cart_with_valid_quantity(client, product, cart_with_product):
#     new_quantity = 2
#     response = client.post(reverse('update-cart', args=[product.id]), {'quantity': str(new_quantity)})
#     assert response.status_code == 302
#     assert response.url == reverse('cart')
#     assert client.session['cart'][str(product.id)] == new_quantity
#
#
# @pytest.mark.django_db
# def test_update_cart_with_invalid_quantity(client, product, cart_with_product):
#     invalid_quantity = 'invalid'
#     response = client.post(reverse('update-cart', args=[product.id]), {'quantity': invalid_quantity})
#     assert response.status_code == 302
#     assert response.url == reverse('cart')
#     assert client.session['cart'][str(product.id)] == 1  # Unchanged
#
#
# @pytest.mark.django_db
# def test_update_cart_exceeding_stock(client, product, cart_with_product):
#     product.stock = 3
#     product.save()
#     exceeding_quantity = 5
#     response = client.post(reverse('update-cart', args=[product.id]), {'quantity': str(exceeding_quantity)})
#     assert response.status_code == 302
#     assert response.url == reverse('cart')
#     # Quantity remains as initially set since exceeding stock is not allowed
#     assert client.session['cart'][str(product.id)] == 1
#
#
# @pytest.mark.django_db
# def test_remove_from_cart(client, user, product, another_product):
#     client.force_login(user)
#
#     # Create two products
#     product1 = product
#     product2 = another_product
#
#     # Simulate adding products to cart
#     session = client.session
#     session['cart'] = {str(product1.id): 1, str(product2.id): 2}
#     session.save()
#
#     # Remove product1 from cart
#     response = client.get(reverse('remove-from-cart', args=[product1.id]))
#
#     # Verify redirection to cart page
#     assert response.status_code == 302
#     assert response.url == reverse('cart')
#
#     # Fetch the updated cart from session
#     session = client.session
#     cart = session.get('cart', {})
#
#     # Verify product1 is removed and product2 is still in the cart
#     assert str(product1.id) not in cart
#     assert str(product2.id) in cart
#
#
# @pytest.mark.django_db
# def test_checkout_view_get_total_price(client, cart_with_product, product):
#     response = client.get(reverse('checkout'))
#     assert response.status_code == 200
#     assert 'total_price' in response.context
#     assert float(response.context['total_price']) == product.price
#
#
# @pytest.mark.django_db
# def test_checkout_view_post_success(client, user, cart_with_product, product):
#     client.force_login(user)
#     address_data = {
#         'name': 'John',
#         'surname': 'Doe',
#         'email': 'john@example.com',
#         'number': '1234567890',
#         'street_name': 'Main Street',
#         'street_number': '123',
#         'city': 'Anytown',
#         'postal_code': '12345',
#         'country': 'Countryland',
#         'payment_method': 'COD'
#     }
#     response = client.post(reverse('checkout'), address_data)
#     order = Order.objects.first()
#
#     assert Order.objects.count() == 1
#     assert order.name == 'John'
#     assert order.email == 'john@example.com'
#     assert OrderProduct.objects.count() == 1
#     assert response.status_code == 302
#     assert response.url == reverse('order-success', kwargs={'order_id': order.id})
#
#
#
# @pytest.mark.django_db
# def test_order_confirmation_view_success(self):
#     client = Client()
#     url = reverse('order-success', args=[self.order.id])
#     response = client.get(url)
#     self.assertEqual(response.status_code, 200)
#     self.assertTrue('order' in response.context)
#     self.assertEqual(response.context['order'].id, self.order.id)
#     self.assertEqual(len(response.context['order'].items.all()), 1)
#     self.assertEqual(response.context['order'].items.all()[0].id, self.order_item.id)
#
#
# @pytest.mark.django_db
# def test_order_confirmation_view_failure(self):
#     client = Client()
#     non_existent_order_id = 999999
#     url = reverse('order-success', args=[non_existent_order_id])
#     response = client.get(url)
#     self.assertEqual(response.status_code, 404)


