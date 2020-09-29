from django.contrib import admin
from plumbing.models import Category, Product, Company, Comments, Basket, ProductInstance, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Comments)
admin.site.register(Basket)
admin.site.register(ProductInstance)
admin.site.register(Order)
