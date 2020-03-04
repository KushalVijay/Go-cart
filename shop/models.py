from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200,db_index=True)
    slug=models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])



class Subcategory(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    slug=models.SlugField(max_length=200,null=True,blank=True)
    Category = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE, null=True,
                                    blank=True)
    class Meta:
        ordering=('name',)
        verbose_name='subcategory'
        verbose_name_plural='subcategories'
    def __str__(self):
        return self.name



class Brand(models.Model):
    name=models.CharField(max_length=200,db_index=True)
    slug=models.SlugField(max_length=200,unique=True)
    class Meta:
        ordering=('name',)
        verbose_name='brand'
        verbose_name_plural='brands'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])



class Product(models.Model):
    category=models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,related_name='products',on_delete=models.CASCADE,default=None)
    name=models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    hide_slug = models.IntegerField(default=0)
    image1 = models.CharField(max_length=500,blank=True,null=True)
    image2 = models.CharField(max_length=500, blank=True, null=True)
    image3 = models.CharField(max_length=500, blank=True, null=True)
    image4 = models.CharField(max_length=500, blank=True, null=True)
    image5 = models.CharField(max_length=500, blank=True, null=True)
    image6 = models.CharField(max_length=500, blank=True, null=True)
    image7 = models.CharField(max_length=500, blank=True, null=True)
    image8 = models.CharField(max_length=500, blank=True, null=True)
    image9 = models.CharField(max_length=500, blank=True, null=True)
    image10 = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    mrp = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    stock=models.IntegerField(default=True)
    available = models.BooleanField(default=True)
    LBH = models.TextField(max_length=50,null=True,blank=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    qty = models.IntegerField(default=0)


    class Meta:
        ordering=('name',)
        index_together=(('id','slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id,self.slug])

class Coupon(models.Model):
    code = models.CharField(max_length=8,null=True,blank=True)
    description = models.CharField(max_length=200,null=True,blank=True)
    discprice = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return self.code


