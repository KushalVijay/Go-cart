from django.conf.urls import  url


app_name='cart'
from .views import (
 cart_update,
cart_remove,
 cart_home,
 checkout_home,
 checkout_done_view,
handlerequest,
SendtoPaytm,
fav_update,
fav_home,
fav_remove,
)
urlpatterns = [

    url(r'^$', cart_home,name='home' ),
    url(r'^checkout/S', checkout_home, name='checkout'),
    url(r'^update/$',cart_update,name='update' ),
    url(r'^remove/$',cart_remove,name='remove' ),
    url(r'^fav/$', fav_home,name='favourite' ),
    url(r'^fav/update/$',fav_update,name='fav_update' ),
    url(r'^fav/remove/$',fav_remove,name='fav_remove' ),
    url(r'^checkout/success/$', checkout_done_view, name='success'),
    url(r'^handlerequest/$', handlerequest, name='HandleRequest'),
    url(r'^paymentgateway/$', SendtoPaytm, name='Paytm'),
    url(r'^coupon/$', fav_home,name='coupon_apply' ),
]