from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import *

# Register your models here.
#https://getbootstrap.com/docs/5.0/components/alerts/ (bootstrap)
#https://youtu.be/xriCKexNT6s  (Ticket Model video)


#admin.site.register(UserManage)


#mentino Tublery Line to shows Images and Tag on Product db module

class ImagesTublerinline(admin.TabularInline):
    model = Images

class TagTublerinline(admin.TabularInline):
    model = Tag

class ProductAdmin(admin.ModelAdmin):
    inlines =  [ImagesTublerinline,TagTublerinline]

class OrderItemTublerinline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):  #order item field with filter field
    inlines = [OrderItemTublerinline]
    list_display = ['firstname','phone','email','payment_id','paid','date']
    search_fields = ['firstname','email','payment_id']

class Contact_usAdmin(admin.ModelAdmin):#step1(Moldelname+Admin)
    search_fields = ['email','name']

admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)
admin.site.register(Product,ProductAdmin) #one model will shows two table

admin.site.register(Images)
admin.site.register(Tag)

admin.site.register(Contact_us,Contact_usAdmin)#step2(Modelname,Module+searchfieldAdmin)

admin.site.register(Order,OrderAdmin) #one model will shows two table
admin.site.register(OrderItem)

admin.site.register(Ticket)
