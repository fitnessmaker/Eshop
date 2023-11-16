from django.shortcuts import render,redirect,HttpResponseRedirect
from store_app.models import Product,Categories,Filter_Price,Color,Brand,Order,OrderItem,Ticket,Contact_us
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django import forms
from .form import CreateTicketForm,UpdateTicketForm
from datetime import datetime


import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))



def BASE(request):
    return render(request,'Main/base.html')


def HOME(request):
    product = Product.objects.filter(status = 'Publish').order_by('name')

    context = {
        'product':product,

    }

    return render(request,'Main/index.html',context)


def PRODUCT(request):
    #product = Product.objects.filter(status='Publish') no need this to fetch published
    categories = Categories.objects.all()
    price_filter = Filter_Price.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()

    CATID = request.GET.get('categories')#READ FROM HTML
    PRICE_FILTER_ID = request.GET.get('price_filter')#GET server selection by html page
    COLOR_ID = request.GET.get('color1')#change to 'color1' in product.html to understand
    BRAND_ID = request.GET.get('brand')
    ATOZ_ID = request.GET.get('ATOZ')
    ZTOA_ID = request.GET.get('ZTOA')
    LTOH_ID =request.GET.get('LTOH')
    HTOL_ID = request.GET.get('HTOL')
    NEW_PRO = request.GET.get('NEW_PRODUCT')
    OLD_PRO = request.GET.get('OLD_PRODUCT')


    if CATID:
        product = Product.objects.filter(categories = CATID,status = 'Publish')
    elif PRICE_FILTER_ID:
        product = Product.objects.filter(filter_price = PRICE_FILTER_ID,status = 'Publish') #filter_price (from model for db fileter)
    elif COLOR_ID:
        product = Product.objects.filter(color = COLOR_ID,status = 'Publish')
    elif BRAND_ID:
        product =Product.objects.filter(brand =BRAND_ID, status = 'Publish')
    elif ATOZ_ID:
        product = Product.objects.filter(status = 'Publish').order_by('name')#product variable must mention in html inside forloop to fetch
    elif ZTOA_ID:
        product = Product.objects.filter(status = 'Publish').order_by('-name')
    elif LTOH_ID:
        product = Product.objects.filter(status = 'Publish').order_by('price')
    elif HTOL_ID:
        product = Product.objects.filter(status = 'Publish').order_by('-price')
    elif NEW_PRO:
        product = Product.objects.filter(status = 'Publish', condition = 'New').order_by('-id')
    elif OLD_PRO:
        product = Product.objects.filter(status = 'Publish', condition = 'Old').order_by('-id')
    else:
        product = Product.objects.filter(status = 'Publish').order_by('-id')





    context = {
        'product': product,
        'categories' : categories,
        'price_filter': price_filter,
        'color': color,
        'brand':  brand,

    }
    return render(request,'Main/product.html',context)


def SEARCH(request):

    query = request.GET.get('query') #query from input html to find from server db
    product = Product.objects.filter(name__icontains = query)

    context = {
        'product':product,

    }

    return render(request,'Main/search.html',context)


def PRODUCT_DETAIL_PAGE(request,id):
    produ = Product.objects.filter(id = id).first()

    context = {
        'produ': produ,

    }
    return render(request,'Main/product_single.html',context)


def CONTACT_PAGE(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        #to save database need to  import model Contact_us

        contact = Contact_us(
            name = name,
            email = email,
            subject = subject,
            message = message,
        )
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, email_from, ['1tmcjubail@gmail.com'])  # ["email -to "]
            contact.save()
            messages.info(request,'Email Send Successfully.')
            return redirect('contact')
        except:
            messages.warning(request,'Something Went Wrong')
            return redirect('contact')

    return render(request,'Main/contact.html')


def Handle_Register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Username Already Taken.')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email Already Registered.')
                return redirect('register')
            else:
                #variable + import user Model from django
                customer = User.objects.create_user(username=username,email=email,password=pass1,first_name=first_name,last_name=last_name)
                customer.save()
                messages.warning(request, 'Successfully Registered...!')
                return redirect('login')
        else:
            messages.warning(request,'Password not Matching')
        return redirect('register')
    else:

        return render(request,"Registration/auth.html")


def LOGIN(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request,'check your username and password')
            return redirect('login')




    return render(request,'Registration/auth.html')


def LOGOUT(request):
    logout(request)
    redirect('home')
    return redirect('home')




#CART Session
#copy from https://pypi.org/project/django-shopping-cart/
@login_required(login_url="/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login/")
def cart_detail(request):
    return render(request, 'Cart/cart_details.html')


@login_required(login_url="/login/")
def Check_out(request):
    amount_str = request.POST.get('amount')  #string value need to convert to integer
    amount_float = float(amount_str)
    amount = int(amount_float)
    payment = client.order.create({
            "amount": amount,
            "currency": "SAR",
            "payment_capture" : "1"
        })

    order_id = payment['id']
    context = {
        'order_id' : order_id,
        'payment' : payment,
    }
    return render(request,'Cart/checkout.html',context)

@login_required(login_url="/login/")
def PlaceOrder(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')#seesion for who logged as user
        user = User.objects.get(id = uid) # save as per User Modal user name
        cart = request.session.get('cart') #by session user items will fetch from CART model

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        order_id = request.POST.get('order_id')
        payment = request.POST.get('payment')

        context = {
            'order_id': order_id,

        }
        #save into order table
        order = Order(
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            city = city,
            address = address,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,      #payment_id database field order_id form field
            amount = amount,
        )
        order.save()
        for i in cart:      #order item quntiy and price multipay
            a = (int(cart[i]['price']))
            b = (int(cart[i]['quantity']))
            total = a * b

            item = OrderItem(  #Order + OrderItem
                user = user,
                order = order,
                product= cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i] ['quantity'],
                price = cart[i] [ 'price'],
                total = total,
            )
            item.save()
        return render(request,'Cart/placeorder.html',context)

@csrf_exempt
def Success(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ""
        for key, val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break

        user = Order.objects.filter(payment_id = order_id).first()
        user.paid = True
        user.save()


    return render(request,'Cart/thank.html')

@login_required(login_url="/login/")
def YourOrder(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    order = OrderItem.objects.filter(user = user)
    context = {
        'order':order,
    }

    return render(request,'Main/your_order.html',context)



#def Open(request):

    #return render(request,'Registration/EnterTicket.html')

#def Track_Ticket(request):

    #return render(request,'Registration/track.html')



#TRAKING SYSTEM ATTACHING WITH IT

#view ticket details
@login_required(login_url="/login/")
def ticket_details(request,pk):
    ticket = Ticket.objects.get(pk=pk)
    t = User.objects.get(username=ticket.created_by)
    tickets_by_user = t.created_by.all()
    context = {'ticket':ticket, 'tickets_by_user':tickets_by_user}
    return render(request,'tik/ticket_details.html',context)



#create ticket
@login_required(login_url="/login/")
def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.created_by = request.user
            var.ticket_status = 'Pending'
            var.save()
            messages.info(request,'ticket submitted successfully')
            return redirect('create-ticket')
        else:
            messages.warning(request,'somthing went wrong')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form':form}
        return render(request,'tik/create_ticket.html',context)

#update Ticket

@login_required(login_url="/login/")
def update_ticket(request,pk):
    ticket = Ticket.objects.get(pk=pk)
    if not ticket.is_resolved:
        if request.method == 'POST':
            form = UpdateTicketForm(request.POST,instance=ticket)
            if form.is_valid():
                form.save()

                messages.info(request,'ticket Updated successfully')
                return redirect('all-tickets')
            else:
                messages.warning(request,'somthing went wrong')
                #return redirect('create-ticket')
        else:
            form = UpdateTicketForm(instance=ticket)
            context = {'form':form}
            return render(request,'tik/update_ticket.html',context)
    else:
        messages.warning(request,'you cannot make any changes..!')
        return redirect('home')


#veiew all created ticket
@login_required(login_url="/login/")
def all_tickets(request):
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-date_created')
    context = {'tickets':tickets}
    return render(request,'tik/all_tickets.html',context)


#for Engineers


#view ticket Q
@login_required(login_url="/login/")
def ticket_queue(request):
    tickets = Ticket.objects.filter(ticket_status='Pending').order_by('-date_created')
    context = {'tickets':tickets}
    return render(request,'tik/ticket_queue.html',context)

#accept ticket from  Q
@login_required(login_url="/login/")
def accept_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.assigned_to = request.user
    ticket.ticket_status = 'Active'
    ticket.accepted_dated = datetime.now()
    ticket.save()
    messages.info(request,'Ticket accepted and added on your workspace')
    return redirect('ticket-queue')



#close tiket
@login_required(login_url="/login/")
def close_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    ticket.ticket_status = 'Completed'
    ticket.is_resolved = True
    ticket.closed_date = datetime.now()
    ticket.save()
    messages.info(request,'Ticket Resolved...')
    return redirect('ticket-queue')


#tickets engineers working on
@login_required(login_url="/login/")
def workspace(request):
    tickets = Ticket.objects.filter(assigned_to=request.user,is_resolved=False)
    context = {'tickets':tickets}
    return render(request,'tik/workspace.html',context)

#all clossed /resolved tickets
@login_required(login_url="/login/")
def all_closed_tickets(request):
    tickets = Ticket.objects.filter(assigned_to=request.user, is_resolved=True).order_by('-date_created')
    context = {'tickets':tickets}
    return render(request,'tik/all_closed_tickets.html',context)


#Layout test
def layout(request):

    return render(request,'tik/layout.html')