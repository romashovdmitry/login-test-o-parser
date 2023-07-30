# DRF imports
from rest_framework import serializers

# import models
from api.models.product import Product


class GetProductSerializer(serializers.ModelSerializer):
    ''' serializer for get objects of Product model'''

    class Meta:
        model = Product
        fields = [
            'name',
            'current_price',
            'without_discount_price',
            'discount',
            'product_url',
            'rating',
            'in_stock',
            'image'
        ]


class PostProductSerializer(serializers.Serializer):
    ''' serializer for post request to API '''
    products_count = serializers.IntegerField(
        default=10,
        min_value=1,
        max_value=50
    )