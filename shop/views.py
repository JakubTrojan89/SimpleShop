from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Q

from .forms import AddProductForm, EditProductForm
from shop.models import Product, Category


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
