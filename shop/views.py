from audioop import reverse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Q
from django.views import View
from django.views.generic import TemplateView

from .forms import AddProductForm, EditProductForm
from shop.models import Product, Category, OrderProduct, Order, Address


def search(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    products = Product.objects.filter(is_sold=False)

    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'shop/search.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })


def index(request):
    products = Product.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'shop/index.html', {
        'categories': categories,
        'products': products
    })


def contact(request):
    return render(request, 'shop/contact.html')


def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'product/detail.html',{
        'product': product,
        'related_products': related_products,
    })


@login_required()
def add(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()

            return redirect('shop:detail', pk=product.pk)
    else:
        form = AddProductForm()

    return render(request, 'product/add.html',{
        'form': form,
        'title': 'Add Product',
    })


@login_required
def edit(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            return redirect('shop:detail', pk=product.id)
    else:
        form = EditProductForm(instance=product)

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Edit item',
    })


@login_required
def delete(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    product.delete()

    return redirect('dashboard:dashboard')


class CartView(TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        cart_products = []
        total_price = 0

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            total_product_price = product.price * quantity
            total_price += total_product_price
            cart_products.append({
                'product': product,
                'quantity': quantity,
                'total_product_price': total_product_price,
            })

        context['cart_cart_products'] = cart_products
        context['total_price'] = total_price
        return context


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                messages.error(request, "Quantity must be greater than zero.")
                return redirect('shop:cart')
        except ValueError:
            messages.error(request, "Invalid quantity. Please provide a valid number.")
            return redirect('shop:cart')

        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + quantity
        request.session['cart'] = cart

        messages.success(request, f"{quantity} {product.name}{'s' if quantity > 1 else ''} added to cart.")
        return redirect('shop:cart')


class UpdateCartView(View):
    def post(self, request, product_id):
        submitted_quantity = request.POST.get('quantity', '').strip()
        cart = request.session.get('cart', {})

        current_quantity = cart.get(str(product_id), 1)

        if submitted_quantity.isdigit() and int(submitted_quantity) > 0:
            current_quantity = int(submitted_quantity)
            product = get_object_or_404(Product, id=product_id)

        request.session['cart'] = cart
        request.session.modified = True

        return redirect(reverse('cart'))


class RemoveFromCartView(View):
    def get(self, request, product_id):
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            del cart[str(product_id)]

        request.session['cart'] = cart
        return redirect(reverse('cart'))


class CheckoutView(View):
    def get(self, request):
        # Calculate total price from session cart
        cart = request.session.get('cart', {})
        total_price = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total_price += product.price * quantity

        # Pass total price to template
        context = {
            'total_price': total_price,
        }
        return render(request, 'shop/checkout.html', context)

    def post(self, request):
        # Extract form data
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        street = request.POST.get('street_name')
        street_number = request.POST.get('street_number')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method')

        try:
            # First, create an Address instance
            address = Address.objects.create(
                street=street,
                street_number=street_number,
                city=city,
                postal_code=postal_code,
                country=country
            )

            # Then create an Order instance
            order = Order.objects.create(
                user=request.user,
                address=address,
                payment_method=payment_method,
                name=name,
                surname=surname,
                email=email,
                phone_number=phone_number,
                paid=False,
                status=Order.PROCESSING
            )

            # Process cart items from session
            cart = request.session.get('cart', {})
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                OrderProduct.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

            # Clear the cart from session after processing
            request.session['cart'] = {}

            messages.success(request, "Your order has been placed successfully!")
            return redirect(reverse('order-success', kwargs={'order_id': order.id}))

        except Exception as e:
            messages.error(request, f"There was an error processing your order: {str(e)}")
            return redirect('checkout')


class OrderConfirmationView(View):
    def get(self, request, order_id):
        # Retrieve the order using the order_id
        order = get_object_or_404(Order, id=order_id)
        # Add any additional context you want to pass to the template
        context = {
            'order': order,
        }
        return render(request, 'shop/order-success.html', context)