from django.contrib import admin
from .models import Category ,Product,Brand,Coupon,Subcategory

# Register your models here.

admin.site.register(Coupon)
admin.site.register(Subcategory)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Brand)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','available','created','updated']
    list_filter = ['available','created','updated']
    list_editable=['price','available']
    prepopulated_fields = {'slug':('name',)}

