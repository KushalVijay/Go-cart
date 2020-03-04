from django.conf.urls import url
from django.urls import path


from .views import (
        Login_View,
        AccountEmailActivateView,
        Register_View,
        Logout_view,
        Home,
        profile
        )


app_name = 'accounts'
urlpatterns = [
    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$',
            AccountEmailActivateView.as_view(),
            name='email-activate'),
    url(r'^email/resend-activation/$',
            AccountEmailActivateView.as_view(),
            name='resend-activation'),
    path('logout',Logout_view,name='logout'),
    path('login',Login_View.as_view(),name='login'),
    path('home', Home.as_view(), name='home'),
    path('profile', profile, name='profile'),
    path('register',Register_View.as_view(),name='register'),
    
]
