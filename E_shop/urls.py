"""
URL configuration for E_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .import views
from .form import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #path('ticket/', include('ticket.urls')),
    path('admin/', admin.site.urls),
    path('',views.HOME,name='home'),
    path('base/',views.BASE,name='base'),
    path('products/',views.PRODUCT,name='products'),
    path('search/',views.SEARCH,name='search'),
    path('products/<str:id>',views.PRODUCT_DETAIL_PAGE,name='product_detail'),

    path('contact/',views.CONTACT_PAGE,name='contact'),

    #Registration
    path('register/',views.Handle_Register,name="register"),
    path('login/',views.LOGIN,name="login"),
    path('logout/',views.LOGOUT,name="logout"),

    #Track Ticket Function
    #path('open/',views.Open,name="open"),
    #path('track/', views.Track_Ticket, name="track"),

    #TRACKING SYSTEM
    path('ticket-details/<int:pk>/', views.ticket_details,name='ticket-details'),
    path('create-ticket/', views.create_ticket,name='create-ticket'),
    path('update-ticket/<int:pk>/', views.update_ticket,name='update-ticket'),
    path('all-tickets/', views.all_tickets,name='all-tickets'),
    path('ticket-queue/', views.ticket_queue,name='ticket-queue'),
    path('accept-ticket/<int:pk>/', views.accept_ticket,name='accept-ticket'),
    path('close-ticket/<int:pk>/', views.close_ticket,name='close-ticket'),
    path('workspace/', views.workspace,name='workspace'),
    path('all-closed-tickets/', views.all_closed_tickets,name='all-closed-tickets'),

    path('layout/', views.layout,name='layout'),




    #CART Modlue download
path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('cart/checkout/',views.Check_out,name='checkout'),
    path('cart/checkout/placeorder',views.PlaceOrder,name='place_order'),
    path('success',views.Success,name='success'),


    path('your_order',views.YourOrder,name='your_order')

] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
