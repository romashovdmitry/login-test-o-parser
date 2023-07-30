from rest_framework.routers import DefaultRouter

from api.views import ProductViewSet

router = DefaultRouter()
router.register(r'v1/products', ProductViewSet, basename='products')
