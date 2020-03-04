from django.shortcuts import render,redirect
from .models import complain

def contact(request):
    if request.method=='POST':
        obj = complain()
        obj.name = request.POST['name']
        obj.email = request.POST['email']
        obj.subject = request.POST['subject']
        obj.message = request.POST['msg']
        obj.save()
        return redirect('shop:product_list')
    return render(request,"customer_care/contact.html")
