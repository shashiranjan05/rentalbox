from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from .forms import  CustomUserCreationForm
from django.conf import settings
import razorpay
from .forms import ProductForm

# User = settings.AUTH_USER_MODEL

# Create your views here.
def index(request):
    user_obj=request.user
    if request.user.is_authenticated:
        username = request.user.email
        name = username.split('@')[0]
        role = request.user.role
    else:
        name = 'AnonymousUser'
        role = ''
    context = {'name':name,'role':role}
    return render(request, 'warehouse/index.html', context)

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

def requirement_details(request):
    return render (request, 'warehouse/reuirement.html')

def create_order_id():
    current_time = datetime.datetime.now()
    current_year= current_time.year
    current_month= current_time.month
    current_day= current_time.day
    current_hour= current_time.hour
    current_minute= current_time.minute
    current_second= current_time.second

    current_order_id = str(current_year) + str(current_month) + str(current_day) + str(current_hour) + str(current_minute) + str(current_second)

    return current_order_id

#generate enquiry or RFQ
@login_required(login_url='/login/')
def enquiry_view(request):
    username= request.user.email
    name = username.split('@')[0]
    role=request.user.role
    if request.method == 'POST':
        enquiry_id = create_order_id() 
        customer_name = request.POST.get("your_name")
        your_email = request.POST.get("your_email")
        phone_number = request.POST.get("phone_number")
        org_details = request.POST.get("org_details")
        your_requirement = request.POST.get("your_requirement")
        print(request.user)
        visit_info = EnquiryDetails(user=request.user,enquiry_id= enquiry_id,customer_name = customer_name, your_email = your_email, phone_number = phone_number,
        org_details = org_details, your_requirement = your_requirement)
        visit_info.save()
       
        # return HttpResponseRedirect(reverse('thank_you'))
        print("enquire form details saved in database  .....")
    return render(request, 'warehouse/enquiry.html',{'name':name, 'role':role})

# generate sales quote
@login_required(login_url='/login/')
def sales_quote_view(request):
    username= request.user.email
    name = username.split('@')[0]
    role=request.user.role
    all_data = EnquiryDetails.objects.all()
    sales_quote_id = create_order_id() 
    if request.method == 'POST':
        # enquiry = all_data
        idAndDetails = request.POST.get("enquiry_id")
        print(idAndDetails)
        # sales_quote_id = request.POST.get("sales_quote_id")
        enquiry_id = idAndDetails.split('@')[0]
        print("enquiry_id---- ", enquiry_id)
        enquiry=EnquiryDetails.objects.get(enquiry_id=enquiry_id)
        product_name = request.POST.get("product_name")
        product_id = request.POST.get("product_id")
        product_details = request.POST.get("product_details")
        time_period = request.POST.get("time_period")
        pricing= request.POST.get("pricing")
        qty= request.POST.get("qty")
        sales_info = SalesQuoteDetails(enquiry= enquiry,product_name = product_name, product_id = product_id,
        product_details = product_details, time_period = time_period, pricing=pricing, qty=qty,sales_quote_id=sales_quote_id)
        sales_info.save()
        return redirect('dashboard')
       
        # return HttpResponseRedirect(reverse('thank_you'))
        print("sales form details saved in database  .....")
    return render(request, 'warehouse/sales_quote.html',{'all_data':all_data, 'name':name, 'role':role})


#filter by appliances , furniture, electronics
def product_items_by_filter(request, category):
    user_obj=request.user
    if request.user.is_authenticated:
        username = request.user.email
        name = username.split('@')[0]
        role = request.user.role
    else:
        name = 'AnonymousUser'
        role = ''

    product_obj = Products.objects.filter(categories=category)
    context={'product_obj':product_obj,'name':name, 'role':role}

    return render(request, 'warehouse/product.html',context )




#create product details
@login_required(login_url='/login/')
def create_products_details(request):

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')  # Redirect to a product list page or wherever you prefer
    else:
        form = ProductForm()
    return render(request, 'warehouse/create_product.html', {'form': form})

def product_details_view(request):
    user_obj=request.user
    if request.user.is_authenticated:
        username = request.user.email
        name = username.split('@')[0]
        role = request.user.role
    else:
        name = 'AnonymousUser'
        role = ''

    product_obj = Products.objects.all()
    context={'name':name, 'role':role, 'product_obj':product_obj}
    return render(request, 'warehouse/product.html', context)

@login_required(login_url='/login/')
def request_for_quote_view(request):
    data = EnquiryDetails.objects.filter(user=request.user)
    return data

@login_required(login_url='/login/')
def myorder(request):
    print("************enter in my order---------")
    username= request.user.email
    name = username.split('@')[0]
    role=request.user.role
    order_objs = MyOrder.objects.filter(user=request.user)

    context={'name':name, 'role':role, 'order_objs':order_objs}

    return render(request,'warehouse/myorder.html',context)




#order created
@login_required(login_url='/login/')
def create_order(request):
    print("************enter in create order---------")
    username= request.user.email
    name = username.split('@')[0]
    role=request.user.role
    cart_details = CartDetails.objects.filter(user=request.user, is_paid=False)
   
    if cart_details.exists():
        cart_objs = MyOrder.objects.create(user=request.user)
        amount=[]
        for single_product in cart_details:
            amount.append(single_product.total_amount)

        total_amount=sum(amount)
        for cart_items in cart_details:
            cart_objs.cart.add(cart_items)
            cart_items.is_paid=True
            cart_items.save()   
        cart_objs.total_amount= total_amount
        cart_objs.is_paid = True
        
        
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        
        payment = client.order.create({'amount':total_amount*100, 'currency':'INR', 'payment_capture':1})
        context= { 'cart':cart_objs,'payment':payment,'cart_details':cart_details,'name':name, 'role':role,'total_amount':total_amount  }
        cart_objs.razor_pay_order_id = payment['id']
        cart_objs.save()

        print("***************my order has been created")

        return render(request,'warehouse/invoice.html',context)
    return redirect('mycart')

@login_required(login_url='/login/')
def update_cart_details(request):
    username= request.user.email
    name = username.split('@')[0]
    role=request.user.role
     #for updating cart items and qty and time period
    cart_details = CartDetails.objects.filter(user=request.user, is_paid=False)
    if request.method == 'POST':
        print("enter for update ===============", cart_details)
        for items in cart_details:
            time_period = request.POST.get(f"time_period_{items.id}")
            qty= request.POST.get(f"quantity_{items.id}")
            pricing= items.pricing
            items.time_period= time_period
            # items.pricing = pricing
            items.qty= qty
            print(time_period, pricing, qty)
            timeing=int(items.time_period.split(' ')[0])
            if time_period=='1 Year':
                total_amount = int(qty)*int(pricing)*12
            else:
                print("qty", qty, type(qty))
                print("pricing", pricing, type(pricing))
                print("timeing", timeing, type(timeing))
                total_amount = int(qty)*int(float(pricing))*int(timeing)
            items.total_amount= total_amount
            items.save()
    print("items has been updated========================")
    return redirect('mycart')



#cart details only view  page /// on click of payment above route will trigger that will generate order id
@login_required(login_url='/login/')
def cart_details_view(request):

    username= request.user.email
    name = username.split('@')[0]
    role=request.user.role
    amount=[]
    cart_details = CartDetails.objects.filter(user=request.user, is_paid=False)
    for single_product in cart_details:
        amount.append(single_product.total_amount)
    total_amount=sum(amount)
    print("enter in cart details view part")

    context={'name':name, 'role':role, 'total_amount':total_amount,'cart_details':cart_details}
    return render(request,'warehouse/mycart.html',context)


#create cart from normal image to addtocart normal flow
@login_required(login_url='/login/')
def put_in_cart_view(request,id):
    username= request.user.email
    user_name = username.split('@')[0]
    role=request.user.role

    product_obj= Products.objects.get(id=id)
    qty=1
    time_period='1 Year'
    pricing= product_obj.price
    timeing=int(time_period.split(' ')[0])
    if time_period=='1 Year':
        total_amount = int(qty)*int(pricing)*12
    else:
        total_amount = int(qty)*int(pricing)*int(timeing)

    
    data = CartDetails(user=request.user,product_obj=product_obj, pricing=pricing,qty=qty,time_period=time_period,total_amount=total_amount)
    data.save()

    update_stock= product_obj.stock 
    if update_stock ==0:
        pass
    else:
        product_obj.stock = update_stock-1
        product_obj.save()

    return redirect('mycart')

## add to cart view main logic for cart from rfq flow 
from django.conf import settings
@login_required(login_url='/login/')
def add_to_cart_view(request,id):
    user= request.user
    sales_quote= SalesQuoteDetails.objects.get(sales_quote_id=id, added_to_cart=False, sq_reject=False)
    print("sales quote add to cart====", sales_quote)
    enquiry=sales_quote.enquiry
    pricing = sales_quote.pricing
    qty=sales_quote.qty
    time_period= sales_quote.time_period
    timeing=int(time_period.split(' ')[0])
    if time_period=='1 Year':
        total_amount = int(qty)*int(pricing)*12
    else:
        total_amount = int(qty)*int(pricing)*int(timeing)
    print("total amount", total_amount)
    data = CartDetails(user=user,enquiry=enquiry, sq_details=sales_quote,pricing=pricing,qty=qty,time_period=time_period,total_amount=total_amount)
    data.save()
    print("cart created********** -0-----")
    
    sales_quote.added_to_cart =True
    sales_quote.save()

    return redirect('mycart')

@login_required(login_url='/login/')
def reject_sales_quote_view(request,id):
    sales_quote= SalesQuoteDetails.objects.filter(sales_quote_id=id, added_to_cart=False,sq_reject=False)
    print("sales quote-----", sales_quote)
    if sales_quote.exists():
        squote=sales_quote[0]
        squote.sq_reject =True
        squote.save()
    return redirect('dashboard')



### authentication views 

def register_view(request):
    if request.method == 'POST':
        print("in register part")
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            print("in register part complete")

            return redirect('dashboard')

    else:
        intial_data = {'username':'','password1':'','password2':''}
        form = CustomUserCreationForm(initial=intial_data)
    return render(request, 'warehouse/register.html',{'form':form})



def login_view(request):
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        intial_data = {'username':'','password':''}
        form = AuthenticationForm(initial=intial_data)
    return render(request, 'warehouse/login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('product')

@login_required(login_url='/login/')
def dashboard_view(request):
    username= request.user.email
    name = username.split('@')[0]
    role=request.user.role

    # for customer request 
    if role == 'ADMIN':
        data= EnquiryDetails.objects.all()
    else:
        data= request_for_quote_view(request)
        
    sales_quote = SalesQuoteDetails.objects.filter(added_to_cart=False, sq_reject=False)
    
    return render(request, 'dashboard.html',{'data':data,'sales_quote':sales_quote, 'name':name,'role':role})




# def success(request):
#     order_id= request.GET.get('order_id')
#     cart = Cart.objects.get(razor_pay_order_id=order_id)
#     cart.is_paid=True

#     print("enter in success----", order_id)
#     cart.save()

#     return HttpResponse("Payment Successful")




