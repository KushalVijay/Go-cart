from django.db import models
from accounts.models import User
# Create your models here.

class Order(models.Model):
    username = models.CharField(max_length=200,blank=True,null=True)
    order_id = models.CharField(max_length=200,blank=True,null=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    total = models.CharField(max_length=200,blank=True,null=True)
    contact = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)
    details = models.TextField(max_length=2000,null=True,blank=True)

    def __str__(self):
        if self.username is not None:
            return "Username : " + self.username + " Order ID: " + str(self.order_id) + " Email : " + self.email + " Contact : " + self.contact
        return "Order ID: " + str(self.order_id) + "Email : " + self.email + "Contact : " + self.contact

class Order_Count(models.Model):
    email = models.EmailField(max_length=100,blank=True,null=True)
    Ordercount = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.email)