from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.forms import inlineformset_factory


# Create your views here.
def dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all().order_by('-date_created')[:5]
    all_orders = Order.objects.all()

    total_orders = all_orders.count()
    orders_pending = all_orders.filter(status='Pending').count()
    orders_delivered = all_orders.filter(status='Delivered').count()
    context = {
        'customers': customers,
        'orders': orders,
        'total_orders': total_orders,
        'orders_pending': orders_pending,
        'orders_delivered': orders_delivered,
    }
    return render(request, 'accounts/dashboard.html', context)


def customer(request, pk):
    customer = Customer.objects.get(pk=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
    }
    return render(request, 'accounts/customer.html', context)


def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'accounts/products.html', context)


def create_orders(request):
    OrderForm = inlineformset_factory(Customer, Order, fields='__all__', exclude=['customer'], extra=5)

    context = {

    }
    return render(request, 'accounts/create_orders.html', context)
