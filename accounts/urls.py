from django.urls import path
from .views import *
urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('customer/<str:pk>', customer, name='customer'),
    path('products/', products, name='products'),
    path('create_orders/', create_orders, name='create_orders'),
]