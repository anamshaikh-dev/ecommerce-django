from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import OrderItem, Product, Category, Order

def place_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    total_price = 0

    order = Order.objects.create(
        full_name="Guest User",
        total_price=0
    )

    for item in cart.values():
        OrderItem.objects.create(
            order=order,
            product_name=item['name'],
            product_price=item['price'],
            quantity=item['quantity'],
            image=item['image']
        )
        total_price += item['price'] * item['quantity']

    order.total_price = total_price
    order.save()


    order_ids = request.session.get('order_ids', [])
    order_ids.append(order.id)
    request.session['order_ids'] = order_ids

    request.session['cart'] = {}
    return redirect('order_success')


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)]['quantity'] += 1
    else:
        cart[str(id)] = {
            'name': product.name,
            'price': float(product.price),
            'image': product.image.url,
            'quantity': 1
        }

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    total = 0

    for item in cart.values():
        total += item['price'] * item['quantity']

    return render(request, 'store/cart.html', {
        'cart': cart,
        'total': total
    })


def increase_quantity(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        cart[key]['quantity'] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        if cart[key]['quantity'] > 1:
            cart[key]['quantity'] -= 1
        else:
            del cart[key]  

    request.session['cart'] = cart
    return redirect('cart')


def place_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    total_price = 0

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None
    )

    for key, item in cart.items():
        product = Product.objects.get(id=int(key))

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=item['price']
        )

        total_price += item['price'] * item['quantity']

    request.session['cart'] = {}
    return redirect('order_success')
    


def order_history(request):
    orders = Order.objects.all().prefetch_related('items__product')
    return render(request, 'store/order_history.html', {'orders': orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_detail.html', {'order': order})

def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart
    return redirect('cart')


def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'store/orders.html', {'orders': orders})

def order_success(request):
    return render(request, 'store/order_success.html')


def product_list(request):
    category_id = request.GET.get('category')
    query = request.GET.get('q')

    products = Product.objects.all()

    # CATEGORY FILTER
    if category_id:
        products = products.filter(category_id=category_id)

    # SEARCH FILTER
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    categories = Category.objects.all()

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories
    })
