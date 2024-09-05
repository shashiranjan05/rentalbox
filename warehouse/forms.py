
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.db import transaction
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Products

User = get_user_model()

class EnquiryForm(forms.Form):  
    your_name = forms.CharField(label="Enter first name",max_length=50)  
    your_email  = forms.CharField(label="Enter Email ", max_length = 100)
    mobile_no = forms.CharField(label="Enter Mobile No.",max_length=50)  
    org_details  = forms.CharField(label="Enter Organisations Details", max_length = 100)
    your_requirement = forms.CharField(label="Enter Your Requirement",max_length=500)  

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields =('email','role')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email','role')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Mata:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'sku','image','categories', 'description', 'discount_price','brand','price', 'is_available', 'stock', 'tags' ]

    # @transaction.atomic
    # def save(self):
    #     user = super().save(commit=False)
    #     user.is_customer = True
    #     user.save()
    #     return user

