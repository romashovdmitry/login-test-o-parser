# default imports
from django.contrib import admin
from django.urls import path, include

# DRF classes imports
from api.router import router

# Swagger import
from test_parser.yasg import urlpatterns as SWAG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_adminlte.urls'))
]

urlpatterns += router.urls
urlpatterns += SWAG

