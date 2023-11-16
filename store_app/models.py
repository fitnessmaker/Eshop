from django.db import models
import uuid
from django.utils import timezone
from ckeditor.fields import RichTextField
#from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


#class UserManage(AbstractUser):
 #   is_customer = models.BooleanField(default=False)
  #  is_engineer = models.BooleanField(default=False)

   # def __str__(self):
    #    return self.username
class Categories(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('1000 TO 10000', '1000 TO 10000'),
        ('10000 TO 20000', '10000 TO 20000'),
        ('20000 TO 30000', '20000 TO 30000'),
        ('30000 TO 40000', '30000 TO 40000'),
        ('40000 TO 50000', '40000 TO 50000'),
    )

    price = models.CharField(choices=FILTER_PRICE,max_length=60)

    def __str__(self):
        return self.price



class Product(models.Model):
    CONDITION = (('New','New'),('Old','Old'))
    STOCK = ('IN STOCK','IN STOCK'),('OUT OF STOCK','OUT OF STOCK')
    STATUS = ('Publish','Publish'),('Draft','Draft')

    unique_id = models.CharField(unique=True,max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to='Product_images/img')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION,max_length=100)
    information = RichTextField(null= True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK,max_length=200)
    status = models.CharField(choices=STATUS,max_length=200)
    created_date = models.DateTimeField(default=timezone.now)#sametime onemore attachement and uniqe key kaaranam 1 item mathrame save chuyoo so solution timezone import

    categories = models.ForeignKey(Categories,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price,on_delete=models.CASCADE)

    def save(self,*args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('75%Y%m%d23') + str(self.id)
        return  super().save(*args,**kwargs)

    def __str__(self):
        return self.name



#multiple images slides for items preview
class Images(models.Model):
    image = models.ImageField(upload_to='Product_images/img') #copy from Product
    product = models.ForeignKey(Product,on_delete=models.CASCADE)




class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


#Contact Us
class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email

#Order item Address details for user
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.IntegerField(null=True)
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    #additional_info = models.TextField(blank=True)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=300,null=True,blank=True)
    paid = models.BooleanField(default=False,null=True)
    date = models.DateField(auto_now_add=True) #(default=datetime.datetime.today)

    def __str__(self):
        return self.user.username


# order items
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to="Product_images/Order_Img")
    quantity =models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)

    def __str__(self):
        return self.order.user.username



#TRACKING SYSYTEM

class Ticket(models.Model):
    status_choice = (
        ('Active','Active'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending')
    )



    ticket_number = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_by')
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_dated = models.DateTimeField(null=True,blank=True)
    closed_date = models.DateTimeField(null=True,blank=True)
    ticket_status = models.CharField(max_length=15, choices=status_choice)
    contacts = models.IntegerField()
    Bag = models.BooleanField(max_length=25,blank=True,null=True,default=False)
    Battery = models.BooleanField(max_length=25, blank=True, null=True, default=False)
    Charger = models.BooleanField(max_length=25, blank=True, null=True, default=False)

    def __str__(self):
        return self.title




