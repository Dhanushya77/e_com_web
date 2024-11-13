from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from.models import product

# Create your views here.

def e_com_login(req):
    if req.method == 'POST':
        uname = req.POST['uname']
        password = req.POST['password']
        shop = authenticate(username=uname,password=password)
        if shop:
            login(req,shop)
            return redirect(shop_home)
        else:
            messages.warning(req,'Invalid username or password')
            return redirect(e_com_login)
    else:
        return render(req,'login.html')
# ----------------admin----------------------------------------
def e_com_logout(req):
    logout(req)
    return redirect(e_com_login)

def shop_home(req):
    products = product.objects.all()
    return render(req,'shop/home.html',{'product':products})

def add_pro(req):
    if req.method == 'POST':
        pid = req.POST['pid']
        name = req.POST['name']
        dis = req.POST['dis']
        price = req.POST['price']
        offer_price = req.POST['offer_price']
        stock = req.POST['stock']
        img = req.POST['img']
      
        data = product.objects.create(pid=pid,name=name,dis=dis,price=price,offer_price=offer_price,stock=stock,img=img)
        data.save()
        return redirect(add_pro)
    else:
        data = product.objects.all()
        return render(req,'shop/add_pro.html',{'pro':data})
# ------------------user------------------------------------------