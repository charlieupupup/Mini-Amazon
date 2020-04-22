import threading

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from stock.models import stock, warehouse, product
from order.models import order

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
    return render(request, 'checkout.html', {})

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
    return render(request, 'thankyou.html', {})

def orders(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    orders = order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, "orders.html", context)