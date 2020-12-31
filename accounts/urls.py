from django.urls import path
from .views import *
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('customer/', customer, name='customer'),
    path('products/', products, name='products'),
]