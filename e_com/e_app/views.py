from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from.models import *
import os
from django.contrib.auth.models import User

# Create your views here.

def e_com_login(req):
    if 'shop' in req.session:
        return redirect (shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method == 'POST':
        uname = req.POST['uname']
        password = req.POST['password']
        shop = authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            if shop.is_superuser:
                req.session['shop'] = uname
                return redirect(shop_home)
            else:
                req.session['user'] = uname
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password')
            return redirect(e_com_login)
    else:
        return render(req,'login.html')
    
    
#-----------------admin----------------------------------------


def e_com_logout(req):
    logout(req)
    req.session.flush()
    return redirect(e_com_login)

def shop_home(req):
    if 'shop' in req.session:
        products = product.objects.all()
        return render(req,'shop/home.html',{'product':products})
    else:
        return redirect(e_com_login)

def add_pro(req):
    if 'shop' in req.session:
        if req.method == 'POST':
            pid = req.POST['pid']
            name = req.POST['name']
            dis = req.POST['dis']
            price = req.POST['price']
            offer_price = req.POST['offer_price']
            stock = req.POST['stock']
            img = req.FILES['img']
            data = product.objects.create(pid=pid,name=name,dis=dis,price=price,offer_price=offer_price,stock=stock,img=img)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/add_pro.html')
    else:
        return redirect(e_com_login)

    
def edit_pro(req,id):
    if req.method == 'POST':
        pid = req.POST['pid']
        name = req.POST['name']
        dis = req.POST['dis']
        price = req.POST['price']
        offer_price = req.POST['offer_price']
        stock = req.POST['stock']
        img = req.FILES.get('img')
        if img:
            product.objects.filter(pk=id).update(pid=pid,name=name,dis=dis,price=price,offer_price=offer_price,stock=stock)
            data = product.objects.get(pk=id)
            data.img=img
            data.save()
        else:
            product.objects.filter(pk=id).update(pid=pid,name=name,dis=dis,price=price,offer_price=offer_price,stock=stock)
        return redirect(shop_home)
    else:
        data = product.objects.get(pk=id)
        return render(req,'shop/edit_pro.html',{'data':data})
    
def delete_pro(red,pid):
    data=product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)

def bookings(req):
    booking=Buy.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'bookings':booking})
    
# -----------------user---------------------------------------------

def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswrd=req.POST['pswrd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswrd)
            data.save()
            return redirect(e_com_login)
        except:
            messages.warning(req,'Email already exist')
            return redirect(e_com_login)
    else:
        return render(req,'user/register.html')
    
def user_home(req):
    if 'user' in req.session:
        products = product.objects.all()
        return render(req,'user/home.html',{'product':products})
    else:
        return redirect(e_com_login)

def view_pro(req,id):
    data = product.objects.get(pk=id)
    
    return render(req,'user/view_pro.html',{'data':data})

def add_to_cart(req,pid):
    products=product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(products=products,user=user)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(products=products,user=user,qty=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})

def qty_inc(req,cid):
    data=Cart.objects.get(pk=cid)
    if data.products.stock > data.qty:
        data.qty+=1
        data.save()
    return redirect(view_cart) 

def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    if data.qty==0:
        data.delete()
    return redirect(view_cart)
    
def buy_pro(req,pid):
    products=product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=products.offer_price
    buy=Buy.objects.create(products=products,user=user,qty=qty,t_price=price)
    buy.save()
    return redirect(user_bookings)

def user_bookings(req):
    user=User.objects.get(username=req.session['user'])
    bookings=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/bookings.html',{'bookings':bookings})

def cart_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    price=cart.qty*cart.products.offer_price
    buy=Buy.objects.create(products=cart.products,user=cart.user,qty=cart.qty,t_price=price)
    buy.save()
    data=product.objects.get(id=cart.products.id)
    print(data)
    product.stock-=cart.qty
    product.save()
    
    return redirect(user_bookings)