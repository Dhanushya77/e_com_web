from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_login),
    path('logout',views.user_logout),
    path('register',views.register),
    # -----------admin--------------
    path('admin_home',views.admin_home),
    path('add_pro',views.add_pro),
    path('edit_pro/<id>',views.edit_pro),
    path('delete_pro/<pid>',views.delete_pro),
    path('bookings',views.bookings),
    
    #------------user----------------
    path('user_home',views.user_home),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    path('remove_item/<id>',views.remove_item),
    path('user_bookings',views.user_bookings),
    path('buy_now/<pid>',views.buy_pro),
    path('cart_buy/<cid>',views.cart_buy),
    
]