
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.db import transaction
from django.forms import ModelForm


class EnquiryForm(forms.Form):  
    your_name = forms.CharField(label="Enter first name",max_length=50)  
    your_email  = forms.CharField(label="Enter Email ", max_length = 100)
    mobile_no = forms.CharField(label="Enter Mobile No.",max_length=50)  
    org_details  = forms.CharField(label="Enter Organisations Details", max_length = 100)
    your_requirement = forms.CharField(label="Enter Your Requirement",max_length=500)  

class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user

