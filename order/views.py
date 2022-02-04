from cart.cart import Cart
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from menu.models import Product
from .forms import OrderCreateForm
from .models import OrderItem, Order


def order_create(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    # print(cart)
    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # Order.objects.create()
            order.user = request.user
            order.save()
            for product_id, description in cart.items():
                product = Product.objects.get(pk=int(product_id))
                OrderItem.objects.create(order=order,
                                         product=product,
                                         quantity=int(description['quantity']))
                print(product)
            cart.clear()
            return render(request, 'order_created.html', locals())
    else:
        order_form = OrderCreateForm()
        prices = [float(item['quantity']) * float(item['price']) for item in cart.values()]
        total_cost = round(sum(prices), 2)
    return render(request, 'order_process.html', locals())


