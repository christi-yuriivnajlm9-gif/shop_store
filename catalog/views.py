from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .forms import OrderCreateForm
from .models import Category, OrderItem, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'catalog/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'catalog/product_detail.html', {'product': product})


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'catalog/cart.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1) or 1)
    cart.add(product=product, quantity=quantity)
    return redirect('catalog:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('catalog:cart_detail')


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(request, 'catalog/order_success.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'catalog/checkout.html', {'cart': cart, 'form': form})
