import threading
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from stock.models import stock, warehouse, product
from order.models import order
from order.forms import orderForm
from backend.back import Back


global back
back = Back()


def register(request):
    form = UserCreationForm
    context = {
        'form': form
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
    global back
    data = request.POST.copy()
    pkgid = order.objects.count()
    data['pkgid'] = str(pkgid)
    data['user'] = str(request.user.id)
    form = orderForm(data or None)
    print(form)
    if not form.is_valid():
        print('invalid input')
        return redirect('/invalid')
    else:
        pid = int(form.data['pid'])
        whid = int(form.data['whid'])
        count = int(form.data['count'])
        storage = stock.objects.get(pid=pid).count
        if (count > storage):
            # not enough
            print('not enough stock')
            t1 = threading.Thread(
                target=back.buy, args=(pid, whid, storage+count))
            t1.start()
            return redirect('/invalid')
        else:
            # enough stock
            print('start buying')
            form.save()
            entry = stock.objects.get(pid=pid)
            entry.count -= count
            entry.save()
            t2 = threading.Thread(target=back.pack, args=(pkgid,))
            t2.start()
            send_mail('Your order is confirmed!', 'Thank you for using Mini Amazon!', 'pcphd97@163.com',
                      [order.objects.get(pkgid=pkgid).email], fail_silently=False)
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
    global back
    back.refresh()
    orders = order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, "orders.html", context)

def search(request):
    text = request.GET['s']
    if text <= 'children':
        return redirect('/shop/children')
    elif text <= 'men':
        return redirect('/shop/men')
    else:
        return redirect('/shop/women')

