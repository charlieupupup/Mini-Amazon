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
    return render(request, 'index.html', {})

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
    return render(request, 'shop.html', {})

def single(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, 'shop-single.html', {})

def thankyou(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    myorder = order.objects.get(user=request.user)
    myorder.count = myorder.count + 1
    myorder.save()
    return render(request, 'thankyou.html', {})

def orders(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    orders = order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, "orders.html", context)