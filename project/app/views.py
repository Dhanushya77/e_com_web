
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from.models import *
import os
from django.contrib.auth.models import User
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.

def user_login(req):
    if 'admin' in req.session:
        return redirect (admin_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method == 'POST':
        uname = req.POST['uname']
        password = req.POST['password']
        admin = authenticate(username=uname,password=password)
        if admin:
            login(req,admin)
            if admin.is_superuser:
                req.session['admin'] = uname
                return redirect(admin_home)
            else:
                req.session['user'] = uname
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password')
            return redirect(user_login)
    else:
        return render(req,'login.html')
    
def user_logout(req):
    if 'user' or 'admin' in req.session:
        logout(req)
        req.session.flush()
        return redirect(user_login)
    
def register(req):
    if req.method == 'POST':
        uname = req.POST['uname']
        email = req.POST['email']
        pswrd = req.POST['pswrd']
        data = User.objects.create_user(first_name=uname, email=email, username=email, password=pswrd)
        data.save()
        return redirect(user_login)
    return render(req, 'register.html')

# --------------------admin----------------------

def admin_home(req):
    if 'admin' in req.session:
        product = Product.objects.all()
        return render(req,'admin/home.html',{'product':product})
    else:
        return redirect(user_login)

def add_pro(req):
    if req.method == 'POST':
        name = req.POST['name']
        price = req.POST['price']
        img = req.FILES.get('img') 
        data = Product.objects.create(name=name, price=price, img=img)
        data.save() 
        return redirect(admin_home) 
    return render(req, 'admin/add_pro.html')

def edit_pro(req,id):
    if req.method == 'POST':
        name = req.POST['name']
        price = req.POST['price']
        img = req.FILES.get('img')
        if img:
            Product.objects.filter(pk=id).update(name=name,price=price)
            data = Product.objects.get(pk=id)
            data.img=img
            data.save()
        else:
            Product.objects.filter(pk=id).update(name=name,price=price)
        return redirect(admin_home)
    else:
        data = Product.objects.get(pk=id)
        return render(req,'admin/edit_pro.html',{'data':data})
    
def delete_pro(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(admin_home)

def bookings(req):
    booking=Buy.objects.all()[::-1]
    return render(req,'admin/bookings.html',{'bookings':booking})
    


# ------------------user-------------------------

def user_home(req):
    if 'user' in req.session:
        product = Product.objects.all()
        return render(req,'user/home.html',{'product':product})
    else:
        return redirect(user_login)


def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(product=product,user=user)
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})

def remove_item(req,id):
    cart= Cart.objects.get(pk=id)
    cart.delete()
    return redirect(view_cart)
    
def buy_pro(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    price=product.price
    buy=Buy.objects.create(product=product,user=user,t_price=price)
    buy.save()
    return redirect(user_bookings)

def user_bookings(req):
    user=User.objects.get(username=req.session['user'])
    bookings=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/bookings.html',{'bookings':bookings})

def cart_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    price=cart.product.price
    product=cart.product
    product.save()
    buy=Buy.objects.create(product=cart.product,user=cart.user,t_price=price)
    buy.save()
    return redirect(user_bookings)