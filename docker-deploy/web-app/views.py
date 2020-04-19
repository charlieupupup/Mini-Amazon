import threading

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from stock.models import stock, warehouse
from order.models import order

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
    return render(request, 'thankyou.html', {})