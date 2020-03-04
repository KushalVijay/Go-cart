from django.contrib.auth import authenticate, login, get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe

from .mixins import NextUrlMixin, RequestFormAttachMixin
from .forms import LoginForm, RegisterForm, ReactivateEmailForm
from .models import EmailActivation
from .signals import user_logged_in
from .models import User
from order.models import Order




class AccountEmailActivateView(FormMixin, View):
    success_url = 'login'
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        print("get is  running")
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Please login.")
                return redirect("accounts:login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("accounts:login")
        context = {'form': self.get_form(),'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        print("post is  running")
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        print("form valid is  running")
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        print("form invalid is  running")
        context = {'form': form, "key": self.key }
        return render(self.request, 'registration/activation-error.html', context)





class Login_View(RequestFormAttachMixin, FormView):

    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = 'accounts/home.html'
    default_next = 'shop:product_list'


    def get(self, request, *args, **kwargs):
        context = {'next': request.GET['next'] if request.GET and 'next' in request.GET else ''}
        return render(request, "accounts/login.html", context)
    def form_valid(self, form):

        request = self.request
        print(request)
        print(request.POST)

        next_post = request.POST.get('next')

        if next_post is None:
            next_post= self.default_next
        print(next_post)
        return redirect(next_post)



class Home(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    success_url = 'accounts/home.html'
    def get_object(self):
        return self.request.user


class Register_View(CreateView):
    print("Register krne aa gya")
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = 'login'

def profile(request):
    email = request.user.get_short_name()
    username = request.user.get_full_name()

    history = Order.objects.filter(email=email)
    context = {
        'history':history,
        'name':username,
        'email':email,
    }
    return render(request,'accounts/home.html',context=context)

def Logout_view(request):

    logout(request)
    messages.info(request,"Succefully Logged Out")
    return redirect("shop:product_list")



