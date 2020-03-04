from django.shortcuts import render,redirect
from django.db.models import Q
from shop.models import Product
from carts.models import Cart


def do_search(request):
    print(request.POST)
    query = request.POST['q']
    products = Product.objects.filter(name__icontains=query).distinct()
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    length = len(cart_obj.products.all())
    context = {
        "products": products,
        "length":length,
    }

    return render(request,"search/search_result.html",context)


