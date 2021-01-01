from django.urls import path
from .views import *
from django.contrib.auth.views import *

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
    path('settings/', account_settings, name='account_settings'),

    path('reset_password/', PasswordResetView.as_view(
        template_name='accounts/PasswordReset.html'
    ), name='password_reset'),
    path('reset_password_done/', PasswordResetDoneView.as_view(
        template_name='accounts/PasswordResetDone.html'
    ), name='password_reset_done'),
    path('reset_password_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/PasswordResetConfirm.html'
    ), name='password_reset_confirm'),
    path('reset_password_success/', PasswordResetCompleteView.as_view(
        template_name='accounts/PasswordResetSuccess.html',
    ), name='password_reset_complete'),

]
