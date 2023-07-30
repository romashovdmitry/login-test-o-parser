# default import
from django.contrib import admin

# model import
from api.models.product import Product


class ProductAdmin(admin.ModelAdmin):
    ''' display name in admin panel '''
    list_display = ['name']

admin.site.register(Product, ProductAdmin)
