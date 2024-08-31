from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# from .forms import CustomerSignUpForm 
from django.views.generic import CreateView
from .forms import  CustomUserCreationForm
from django.conf import settings

# User = settings.AUTH_USER_MODEL

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
    print("current_order_id----", current_order_id)

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
def sales_quote_view(request):
    username= request.user.email
    name = username.split('@')[0]
    role=request.user.role
    all_data = EnquiryDetails.objects.all()
    sales_quote_id = create_order_id() 
    if request.method == 'POST':
        # enquiry = all_data
        enquiry_id = request.POST.get("enquiry_id")
        # sales_quote_id = request.POST.get("sales_quote_id")
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
       
        # return HttpResponseRedirect(reverse('thank_you'))
        print("sales form details saved in database  .....")
    return render(request, 'warehouse/sales_quote.html',{'all_data':all_data, 'name':name, 'role':role})

def request_for_quote_view(request):
    data = EnquiryDetails.objects.filter(user=request.user)
    return data

#cart details added 
def cart_details_view(request):

    username= request.user.email
    name = username.split('@')[0]
    role=request.user.role
    amount=[]
    cart_details = CartDetails.objects.filter(user=request.user)
    for single_product in cart_details:
        amount.append(single_product.total_amount)
    total_amount=sum(amount)

    print("cart details ----    - ", cart_details)
    print("total amount ", total_amount, type(total_amount))
    return render(request,'warehouse/mycart.html',{'cart_details':cart_details, 'name':name, 'role':role,'total_amount':total_amount})

def add_to_cart_view(request,id):
    user= request.user
    sales_quote= SalesQuoteDetails.objects.filter(sales_quote_id=id, added_to_cart=False, sq_reject=False)
    print("sales quote add to cart====", sales_quote)
    enquiry=sales_quote[0].enquiry
    pricing = sales_quote[0].pricing
    qty=sales_quote[0].qty
    time_period= sales_quote[0].time_period
    timeing=int(time_period.split(' ')[0])
    if time_period=='1 Year':
        total_amount = int(qty)*int(pricing)*12
    else:
        total_amount = int(qty)*int(pricing)*int(timeing)
    data = CartDetails(user=user,enquiry=enquiry, sq_details=sales_quote[0],pricing=pricing,qty=qty,time_period=time_period,total_amount=total_amount)
    data.save()
    if sales_quote.exists():
        squote=sales_quote[0]
        squote.added_to_cart =True
        squote.save()
    return redirect('dashboard')

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


#####

# class CustomerSignUpView(CreateView):
#     model = User
#     form_class = CustomerSignUpForm
#     template_name = 'warehouse/register.html'

#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'customer'
#         return super().get_context_data(**kwargs)

#     def form_valid(self, form):
#         user = form.save()
#         print("Hello3")

#         login(self.request, user)
#         print("Hello4")
#         return redirect('dashboard')
    
####

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
    return redirect('login')

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







