# Python imports
from uuid import uuid4

# defaul Django import
from django.db import models


class Product(models.Model):
    ''' model for saving parsing product data '''
    class Meta:
        db_table = 'products'

    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=512, null=True)
    current_price = models.PositiveIntegerField(null=True)
    without_discount_price = models.PositiveIntegerField(null=True)
    discount = models.PositiveIntegerField(null=True)
    rating = models.FloatField(null=True)
    in_stock = models.PositiveIntegerField(null=True)
    image = models.URLField(null=True)
    product_url = models.URLField(null=True, max_length=500)