from django.urls import path
from . import views

urlpatterns = [
    path('',views.e_com_login),
    path('logout',views.e_com_logout),
    path('shop_home',views.shop_home),
    path('add_pro',views.add_pro),
    path('edit_pro/<id>',views.edit_pro),
    
]


    