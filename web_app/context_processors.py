from .models import Customer, Order

def add_cart_quantity(request):
    
    try:
        device = request.COOKIES['device']
        customer = Customer.objects.filter(device=device).first()
        order = Order.objects.filter(customer=customer, ordered__in=[False]).first()
        cart_quantity = order.get_cart_quantity()
    except:
        cart_quantity = 0
    
    return {
        'ct_quantity': '(' + str(cart_quantity) + ")"
    }