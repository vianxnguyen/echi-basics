from json.encoder import JSONEncoder
import django
import stripe
import json
from django.conf import settings
from typing import List
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template import RequestContext
from django.template.loader import render_to_string
from .models import Item, OrderItem, Order, ShippingInfo, Customer
from .forms import CheckoutForm

stripe.api_key = settings.STRIPE_SECRET_KEY

def render_to_json(request, data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
        mimetype=request.is_ajax() and "application/json" or "text/html"
    )

def success(request):
    device = request.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, ordered__in=[False])
    order.ordered = True
    for order_item in order.items.all():
        item = order_item.item
        item.stock_quantity -= order_item.quantity

        order_item.ordered = True
        order_item.save()
        item.save()

    order.save()
    
    return render(request, "success.html")

def test_view(request):
    context = {
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, "checkout2.html", context)


def create_payment(request):
    print("creating payment intent!!")
    try:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        order, created = Order.objects.get_or_create(customer=customer, ordered__in=[False])

        intent = stripe.PaymentIntent.create(
            amount=int(order.get_total_cents()),
            currency='usd'
        )
        return JsonResponse({
          'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse(error=str(e)), 403

class PaymentView(View):
    def post(self, request, *args, **kwargs):
        device = self.request.COOKIES['device']
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        line_items = get_stripe_items(device)
        print(line_items)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            shipping_address_collection={
            'allowed_countries': ['US'],
            },
            line_items= get_stripe_items(device),
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cart/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })

def calculate_shipping(order_total):
    if order_total >= 50:
        return 0
    else:
        return 5

def get_stripe_items(device):
    line_items = []
    customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, ordered__in=[False])
    for order_item in order.items.all():
        stripe_item = {
            'price_data': {
                'currency': 'usd',
                'unit_amount' : int(order_item.item.price) * 100,
                'product_data' : {
                    'name': order_item.item.title
                },
            },
            'quantity': order_item.quantity,
        }
        line_items.append(stripe_item)
    shipping = {
        'price_data': {
            'currency': 'usd',
            'unit_amount' : calculate_shipping(order.get_total()) * 100,
            'product_data' : {
                'name': "Shipping"
            },
        },
        'quantity': 1
    }
    line_items.append(shipping)
    return line_items

class HomeView(ListView):
    model = Item
    paginate_by = 4
    template_name = "home.html"

class ShopView(ListView):
    model = Item
    template_name = "shop.html"

class CartView(View):
    """
    model = Order
    template_name = "cart.html"
    """
    def get(self, *args, **kwargs):
        update_cart(self.request)
        device = self.request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

        order, created = Order.objects.get_or_create(customer=customer, ordered__in=[False])
        context = {
            'object': order,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        }
        return render(self.request, "cart2.html", context)

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

def add_to_cart(request, slug):
    add_quantity = 1
    item = Item.objects.get(slug=slug)

    device = request.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)

    order_item, created= OrderItem.objects.get_or_create(
        item=item,
        customer=customer,
        ordered__in=[False]
    )
    if order_item.quantity + add_quantity > item.stock_quantity:
        #not enough in stock
        messages.warning(request, "Limited Stock Available!")
        data = get_messages_data(request, False)
    else:
        order, created = Order.objects.get_or_create(customer=customer, ordered__in=[False])
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += add_quantity
            order_item.save()
        else:
            order.items.add(order_item)
        messages.success(request, "Added to Cart!")
        data = get_messages_data(request, True)
    
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_messages_data(request, success):
    django_messages = []

    for message in messages.get_messages(request):
        django_messages.append({
            "level": message.level,
            "message": message.message,
            "extra_tags": message.tags,
    })
    data = {'messages': django_messages, "success": success}
    return data

def remove_from_cart(request, slug):
    item = Item.objects.get(slug=slug)
    device = request.COOKIES['device']
    customer = Customer.objects.get(device=device)
    if customer == None:
        return redirect("web_app:cart")
   
    order_qs = Order.objects.filter(customer=customer, ordered__in=[False])
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=customer,
                ordered__in=[False]
            )[0]
            order.items.remove(order_item)
            order_item.delete()
        else:
            pass
    return redirect("web_app:cart")

def remove_single_from_cart(request, slug):
    item = Item.objects.get(slug=slug)
    device = request.COOKIES['device']
    customer = Customer.objects.get(device=device)
    if customer == None:
        return redirect("web_app:cart")
   
    order_qs = Order.objects.filter(customer=customer, ordered__in=[False])
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                customer=customer,
                ordered__in=[False]
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
                order.items.remove(order_item)
        else:
            pass

    messages.success(request, "Removed from Cart!")
    data = get_messages_data(request, True)
    
    return HttpResponse(json.dumps(data), content_type='application/json')

def update_cart(request):
    try:
        device = request.COOKIES['device']
        customer = Customer.objects.get(device=device)
        order = Order.objects.filter(customer=customer, ordered__in=[False])[0]
        for order_item in order.items.all():
            stock = order_item.item.stock_quantity
            if stock <= 0:
                remove_from_cart(request, order_item.item.slug)
                messages.warning(request, "Out of Stock!")
                
            elif order_item.quantity > stock:
                order_item.quantity = stock
                order_item.save()
                messages.warning(request, "Updated Cart Based on Stock!")
    except:
        pass
