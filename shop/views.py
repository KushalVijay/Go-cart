from django.shortcuts import render ,get_object_or_404
from .models import Category ,Product
from carts.models import Cart
#from cart.forms import CartAddProductForm

# Create your views here.
def product_list(request ,category_slug = None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    if category_slug:
        category = get_object_or_404(Category ,slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'list.html', {'category':category, 'categories':categories,'products':products})

def product_detail(request,id,slug):
    product=get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    
  #  cart_product_form=CartAddProductForm()
    return render(request, 'detail.html', {'product':product})