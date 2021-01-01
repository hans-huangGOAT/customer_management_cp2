from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('customer/<str:pk>', customer, name='customer'),
    path('products/', products, name='products'),

    path('create_orders/<str:pk>/', create_orders, name='create_orders'),
    path('update_order/<str:pk>', update_order, name='update_order'),
    path('delete_order/<str:pk>', delete_order, name='delete_order'),

    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),

    path('user/', user_page, name='user_page'),
]
