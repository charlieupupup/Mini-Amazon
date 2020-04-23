import threading

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from stock.models import stock, warehouse, product
from order.models import order
from order.forms import orderForm
from backend.back import Back

back = Back()

def register(request):
    form = UserCreationForm
    context = {
        'form' : form
    }
    return render(request, "registration/register.html", context)

def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect('/index')

def home(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    products = product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'index.html', context)

def cart(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, 'cart.html', {})

def about(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, 'about.html', {})

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    form = orderForm(initial={'user': request.user})
    context = {
        'form': form
    }
    return render(request, 'checkout.html', context)

def contact(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, 'contact.html', {})

def shop(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    products = product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop.html', context)

def men(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    products = product.objects.filter(catalog=1)
    context = {
        'products': products
    }
    return render(request, 'shop.html', context)

def women(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    products = product.objects.filter(catalog=2)
    context = {
        'products': products
    }
    return render(request, 'shop.html', context)

def children(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    products = product.objects.filter(catalog=3)
    context = {
        'products': products
    }
    return render(request, 'shop.html', context)

def single(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, 'shop-single.html', {})

def thankyou(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    form = orderForm(request.POST or None)
    if not form.is_valid():
        return redirect('/invalid')
    else:

        form.save()
        return render(request, 'thankyou.html', {})

def invalid(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    form = orderForm(request.POST or None)
    context = {
        'msg': "Invalid input, please try again",
        'form': form
    }
    return render(request, 'checkout.html', context)

def orders(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    orders = order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, "orders.html", context)