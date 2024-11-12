from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout

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
            return redirect(e_com_login)
    else:
        return render(req,'login.html')

def e_com_logout(req):
    logout(req)
    return redirect(e_com_login)

def shop_home(req):
    return render(req,'shop/home.html')