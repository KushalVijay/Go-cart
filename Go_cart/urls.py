"""Go_cart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import  url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from shop.views import product_list,product_detail
from search.views import do_search
from customer_care.views import contact
from upload.views import upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('carts/',include('carts.urls',namespace='cart')),
    path('accounts/',include('accounts.urls',namespace='account')),
    path('',include('shop.urls',namespace='shop')),
    path('query',do_search,name='search'),
    path('contact',contact,name='contact'),
    path('upload',upload,name='upload'),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)