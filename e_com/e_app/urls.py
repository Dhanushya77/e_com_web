from django.urls import path
from . import views

urlpatterns = [
    # --------shop-------------------
    path('',views.e_com_login),
    path('logout',views.e_com_logout),
    path('shop_home',views.shop_home),
    path('add_pro',views.add_pro),
    path('edit_pro/<id>',views.edit_pro),
    path('delete_pro/<pid>',views.delete_pro),
    # --------user---------------------
    path('register',views.register),
    path('user_home',views.user_home),
    path('view_pro/<id>',views.view_pro),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('qty_inc/<cid>',views.qty_inc),
    path('qty_dec/<cid>',views.qty_dec),
    path('user_bookings',views.user_bookings),
    path('buy_pro/<pid>',views.buy_pro)
]


    