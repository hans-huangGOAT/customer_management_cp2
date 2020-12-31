from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.forms import inlineformset_factory
from .forms import *


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    context = {

    }
    return render(request, 'accounts/login.html', context)

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

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
    orders = customer.order_set.all().order_by('-date_created')
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


def create_orders(request, pk):
    customer = Customer.objects.get(pk=pk)
    OrderForm = inlineformset_factory(Customer, Order, fields='__all__', exclude=['customer'], extra=5)
    formset = OrderForm(instance=customer, queryset=customer.order_set.none())

    if request.method == 'POST':
        formset = OrderForm(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('dashboard')

    context = {
        'formset': formset,
    }
    return render(request, 'accounts/create_orders.html', context)


def update_order(request, pk):
    order = Order.objects.get(pk=pk
                              )
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {
        'form': form,
    }
    return render(request, 'accounts/update_order.html', context)


def delete_order(request, pk):
    order = Order.objects.get(pk=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')
    context = {
        'item': order,
    }
    return render(request, 'accounts/delete_order.html', context)
