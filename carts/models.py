from django.conf import settings
from django.db import models
from shop.models import Product
from django.db.models.signals import pre_save,post_save,m2m_changed
User = settings.AUTH_USER_MODEL
# Create your models here.


class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id = request.session.get("cart_id", None)

        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj,new_obj

    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User,null=True,blank=True ,on_delete=models.CASCADE)
    products =  models.ManyToManyField(Product,blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total  = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    order_id = models.CharField(max_length=15,blank=True,null=True)
    updates = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

class FavManager(models.Manager):
    def new_or_get(self,request):
        fav_id = request.session.get("fav_id", None)

        qs = self.get_queryset().filter(id=fav_id)
        if qs.count() == 1:
            new_obj = False
            fav_obj = qs.first()
            if request.user.is_authenticated and fav_obj.user is None:
                fav_obj.user = request.user
                fav_obj.save()
        else:
            fav_obj = Favourite.objects.new(user=request.user)
            new_obj = True
            request.session['fav_id'] = fav_obj.id
        return fav_obj,new_obj

    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Favourite(models.Model):
    user = models.ForeignKey(User,null=True,blank=True ,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    objects = FavManager()

    def __str__(self):
        return str(self.user.email)



def m2m_changed_cart_receiver(sender,instance,action,*args,**kwargs):
    if action== 'post_add' or action== 'post_remove' or action== 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        #print(total)
        instance.subtotal = total
        instance.save()


m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)

def pre_save_cart_receiver(sender,instance,*args,**kwargs):
    instance.total = instance.subtotal ##here we can multiply each subtotal with taxes or shipping charge
pre_save.connect(pre_save_cart_receiver,sender=Cart)

