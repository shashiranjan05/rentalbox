from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
import datetime
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import CustomerSignUpForm 
from django.views.generic import CreateView


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


@login_required(login_url='/login/')
def enquiry_view(request):
    if request.method == 'POST':
        enquiry_id = create_order_id() 
        customer_name = request.POST.get("your_name")
        your_email = request.POST.get("your_email")
        phone_number = request.POST.get("phone_number")
        org_details = request.POST.get("org_details")
        your_requirement = request.POST.get("your_requirement")
        print(request.user)
        visit_info = EnquiryDetails(enquiry_id= enquiry_id,customer_name = customer_name, your_email = your_email, phone_number = phone_number,
        org_details = org_details, your_requirement = your_requirement)
        visit_info.save()
       
        # return HttpResponseRedirect(reverse('thank_you'))
        print("enquire form details saved in database  .....")
    return render(request, 'warehouse/enquiry.html')

def sales_quote_view(request):
    all_data = EnquiryDetails.objects.get(id=1)
    enquiry_id= all_data.enquiry_id
    if request.method == 'POST':
        enquiry = all_data
        product_name = request.POST.get("product_name")
        product_id = request.POST.get("product_id")
        product_details = request.POST.get("product_details")
        time_period = request.POST.get("time_period")
        pricing= request.POST.get("pricing")
        sales_info = SalesQuoteDetails(enquiry= enquiry,product_name = product_name, product_id = product_id,
        product_details = product_details, time_period = time_period, pricing=pricing)
        sales_info.save()
       
        # return HttpResponseRedirect(reverse('thank_you'))
        print("sales form details saved in database  .....")
    return render(request, 'warehouse/sales_quote.html',{'enquiry_id':enquiry_id})

def request_for_quote_view(request):
    data = EnquiryDetails.objects.filter(user=request.user)
    return data

### authentication views 

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        #User = get_user_model()

        if form.is_valid():
            user = form.save()
            # is_customer=True   #for customer
            # user_data=User(is_customer=is_customer)
            # user_data.save()
            login(request,user)
            return redirect('dashboard')
    else:
        intial_data = {'username':'','password1':'','password2':''}
        form = UserCreationForm(initial=intial_data)
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
    data= request_for_quote_view(request)
    print("data=====", data)
    sales_quote = SalesQuoteDetails.objects.all()
    return render(request, 'dashboard.html',{'data':data,'sales_quote':sales_quote})







