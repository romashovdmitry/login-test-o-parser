# DRF imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# parsing foo import
from api.parser import SiteParse, delay_helper

# import models
from api.models.product import Product

# serializers imports
from api.serializers import GetProductSerializer, PostProductSerializer


class ProductViewSet(ModelViewSet):
    ''' parse products and return products '''
    queryset = Product.objects.all()
    http_method_names = ['get', 'post']
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        ''' define serializer for methods '''
        if self.request.method == 'POST':
            return PostProductSerializer
        return GetProductSerializer

    def create(self, request, *args, **kwargs):
        ''' processing post requests, start parsing'''
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            product_count = serializer.validated_data['products_count']
            delay_helper.delay(product_count)
            return Response(status=200)
        else:
            return Response(serializer.errors, status=400)
