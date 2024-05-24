from django.urls import path
from .views import *

urlpatterns = [
    path('', CategoryView,name='Category'),
    path('signup/', register,name='register'),
    path('login/', login,name='login'),
    path('logout/', logout,name='logout'),
    path('productall/',productall,name='productall'),
    path('productcatview/<int:id>',productcatwise,name='productcatwise'),
    path('profile/', profile,name='profile'),
    path('productdetailes/<int:id>',productdetailes,name='productdetailes'),
    path('delete_cartitem/<int:id>',delete_cartitem,name='cdelete'),
    path('Cart/',cart,name='cart'),
    path('shiping/',shiping,name='shiping'),
    path('orderSuccessView/',orderSuccessView,name='orderSuccessView'),
    path('MyorderView/',MyorderView,name='MyorderView'),
    path('MyorderdetaislView/',MyorderdetaislView,name='MyorderdetaislView'),
    path('search/', search, name='search'),
    path('razorpayView/',razorpayView,name='razorpayView'),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
]   
