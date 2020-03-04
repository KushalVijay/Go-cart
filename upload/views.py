from django.shortcuts import render

# Create your views here.

def upload(request):
    return render(request,"upload/upload.html")
