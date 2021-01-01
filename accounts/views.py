from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.forms import inlineformset_factory
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *


# Create your views here.
@logout_required
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, "Username or Password is incorrect")
    context = {

    }
    return render(request, 'accounts/login.html', context)


@logout_required
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account is created for " + user.username)
            return redirect('login')
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    orders_pending = orders.filter(status='Pending').count()
    orders_delivered = orders.filter(status='Delivered').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'orders_pending': orders_pending,
        'orders_delivered': orders_delivered,
    }
    return render(request, 'accounts/user_page.html', context)


@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('account_settings')
    context = {
        'form': form,
    }
    return render(request, 'accounts/account_settings.html', context)


@admin_only
@login_required(login_url='login')
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


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
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


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'accounts/products.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
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


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
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


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def delete_order(request, pk):
    order = Order.objects.get(pk=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')
    context = {
        'item': order,
    }
    return render(request, 'accounts/delete_order.html', context)
