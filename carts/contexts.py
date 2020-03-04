from django.shortcuts import get_object_or_404
from shop.models import Product


def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering every page. 
    """
    cart = request.session.get('cart', {})


    cart_items = []
    total = 0
    product_count = 0
    items = ""
    for id, quantity in cart.items():
        print(id)
        try:
            product = get_object_or_404(Product, pk=id)
        except:
            print("yha error")
        total += quantity * product.price
        product_count += quantity
        cart_items.append({'id': id, 'quantity': quantity, 'product': product})
        items += str(product.name) + " (Qty: " + str(quantity) + ") , "


    request.session['items'] = items
    length = True
    if product_count==0:
        length = False

    return { 'cart_items': cart_items, 'total': total, 'product_count': product_count,'length':length}