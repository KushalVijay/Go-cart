from django.shortcuts import render,redirect,HttpResponse,reverse, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .Checksum import verify_checksum,generate_checksum
from .utils import random_string_generator
from django.contrib import messages
import http.client as ht
from order.models import Order,Order_Count


# Create your views here.
# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     return cart_obj
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';
from shop.models import Product,Coupon
from .models import Cart,Favourite


def cart_home(request):
    return render(request, "carts/home.html")


def cart_update(request):
    id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))

    cart = request.session.get('cart', {})

    cart[id] = cart.get(id, quantity)
    
    request.session['cart'] = cart
    messages.info(request, "Item added to Cart")
    return redirect(reverse('shop:product_list'))


def cart_remove(request):
    id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[id] = quantity
    else:
        cart.pop(id)

    request.session['cart'] = cart
    return redirect(reverse('cart:home'))

def fav_home(request):
    fav_obj,new_obj = Favourite.objects.new_or_get(request)
    return render(request, "carts/favourite.html", {"fav":fav_obj})


def fav_update(request):
    print("aa gye fav mai update")
    product_id = request.POST.get("product_id")
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product is gone")
            return redirect("shop:product_list")
        fav_obj, new_obj = Favourite.objects.new_or_get(request)

        fav_obj.products.add(product_obj)
            #added = True
    return redirect("shop:product_list")  #redirecting using namespace feature




def fav_remove(request):
    product_id = request.POST.get("product_id")
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product is gone")
            return redirect("cart:home")
        fav_obj, new_obj = Favourite.objects.new_or_get(request)
        if product_obj in fav_obj.products.all():
            fav_obj.products.remove(product_obj)

    return redirect("cart:favourite")  #redirecting using namespace feature


def checkout_home(request):
    order_id = random_string_generator()
    # qs = Cart.objects.filter(order_id=order_id)
    # if qs.exists():
    #     order_id = random_string_generator()
    return render(request, "carts/checkout.html",{'order_id':order_id,'newtotal':None,'flag':True})

def SendtoPaytm(request):
    param_dict = {}
    data = request.POST

    if request.POST.get('submit') == 'button3':
        coupons = Coupon.objects.all()
        order_id = request.POST.get('order_id')
        total = request.POST.get('total')
        return render(request,"carts/coupon.html",{'coupons':coupons,'order_id':order_id,'total':total})
    if request.POST.get('submit') == 'button4':
        code = request.POST.get('code')
        discount = Coupon.objects.filter(code=code)[0]
        order_id = request.POST.get('order_id')
        newtotal = float(request.POST.get('total')) - float(discount.discprice)
        return render(request, "carts/checkout.html",{'order_id':order_id,'newtotal':newtotal,'flag':False})

    try:
        numoforder = Order_Count.objects.get(email=data['email'])
        numoforder.Ordercount +=1
        numoforder.save()
    except:
        numoforder = Order_Count.objects.create(email=data['email'],Ordercount=1)

    if request.POST.get('submit')=='button1':
        paid = True
        newtotal = request.POST.get('newtotal')
        if newtotal != 'None':
            print("yes")
            total = newtotal
        param_dict = {
            'MID': 'WorldP64425807474247',
            'ORDER_ID': str(data['order_id']) ,
            'TXN_AMOUNT': str(float(total)),
            'CUST_ID': data['email'],
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'https://rainbowcart.herokuapp.com/carts/handlerequest/', #'http://127.0.0.1:8000/carts/handlerequest/', #
        }

        details = request.session['items']
        obj = Order.objects.create(username=request.user, order_id=str(data['order_id']), address=data['address'],total=str(float(total)),
                                   contact=data['contact'],email=data['email'],paid=True,details= details)
        param_dict['CHECKSUMHASH'] = generate_checksum(param_dict, MERCHANT_KEY)
        cart = {}
        request.session['cart'] = cart

        return render(request, 'carts/paytm.html', {'param_dict': param_dict})
    if request.POST.get('submit') == 'button2':
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        order_id=request.POST.get('order_id')
        address=request.POST.get('address')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        total = request.POST.get('total')
        newtotal = request.POST.get('newtotal')
        print(newtotal,type(newtotal))
        if newtotal !='None':
            print("yes")
            total = newtotal

        details = request.session['items']
        obj = Order.objects.create(username=request.user, order_id=str(data['order_id']), address=data['address'],
                                   total=str(float(total)), contact=data['contact'],email=email,paid=False,details= details)
        cart = {}
        request.session['cart'] = cart
        return render(request, "carts/cashondel.html",{'total':total,'address':address,'contact':contact,'order_id':order_id})


        

@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i=='CHECKSUMHASH':
            checksum = form[i]
    verify = verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE']=='01':
            print("Order Successful")
        else:
            print('Order was not Successful'+response_dict['RESPMSG'])
            order_id = response_dict['ORDERID']
            obj = Order.objects.filter(order_id=order_id)[0]
            obj.paid=False
            obj.save()
    return render(request,'carts/paymentstatus.html',{'response':response_dict})


def send_sms():
    conn = ht.HTTPSConnection("api.msg91.com")

    payload = '''{
      "sender": "RNBWCT",
      "route": "4",
      "country": "91",
      "sms": [
        {
          "message": "Hello you won",
          "to": [
            "9511531960"
          ]
        }
      ]
    }'''
    headers = {
        'authkey': "316162A2MenzoRsCJ55e3559d1P1",
        'content-type': "application/json"
    }

    conn.request("POST", "/api/v2/sendsms", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))



def checkout_done_view(request):
    return render(request, "carts/checkout-done.html")


