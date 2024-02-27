from decimal import Decimal

import pytest
from django.contrib.messages import get_messages
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from shop.models import Order, OrderProduct, Category, Product
from shop.views import search


@pytest.mark.django_db
def test_search_view():
    category = Category.objects.create(name='Test Category')
    product1 = Product.objects.create(name='Test Product 1', description='Test Description 1', category=category)
    product2 = Product.objects.create(name='Test Product 2', description='Test Description 2', category=category)
    request = type('Request', (), {'GET': {'query': 'Test', 'category': category.id}})()
    response = search(request)
    assert response.status_code == 200
    assert 'products' in response.context
    assert 'query' in response.context
    assert 'categories' in response.context
    assert 'category_id' in response.context
    assert product1 in response.context['products']
    assert product2 in response.context['products']
    assert response.context['query'] == 'Test'
    assert response.context['category_id'] == category.id

@pytest.mark.django_db
def test_cart_view_empty_cart(client):
    client.session['cart'] = {}
    client.session.save()
    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assert 'cart_items' in response.context
    assert len(response.context['cart_items']) == 0
    assert response.context['total_price'] == Decimal('0.00')


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
# @pytest.mark.django_db
# def test_checkout_view_post_failure(client, cart_with_product):
#     response = client.post(reverse('checkout'), {})
#     messages_list = list(get_messages(response.wsgi_request))
#     assert len(messages_list) > 0
#     assert 'error' in str(messages_list[0])
#
#
# @pytest.mark.django_db
# def test_order_confirmation_view_success(client, order, order_item):
#     url = reverse('order-success', args=[order.id])
#     response = client.get(url)
#     assert response.status_code == 200
#     assert 'order' in response.context
#     assert response.context['order'].id == order.id
#     assert len(response.context['order'].items.all()) == 1
#     assert response.context['order'].items.all()[0].id == order_item.id
#     # Assuming you have a template named 'order-success.html'
#     assertTemplateUsed(response, 'order-success.html')
#
#
# @pytest.mark.django_db
# def test_order_confirmation_view_failure(client):
#     non_existent_order_id = 999999
#     url = reverse('order-success', args=[non_existent_order_id])
#     response = client.get(url)
#     assert response.status_code == 404
