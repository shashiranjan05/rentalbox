from django.db import models
from phone_field import PhoneField
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.
# class User(AbstractUser):
#     is_customer = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_partner = models.BooleanField(default=False)

#custom User
CHOICES = (('CUSTOMER', 'CUSTOMER'),('ADMIN', 'ADMIN'))

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(choices=CHOICES, max_length=10, default='CUSTOMER')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email




#request for quote
class EnquiryDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    enquiry_id = models.CharField(max_length=64, null = True)
    customer_name = models.CharField(max_length=64, null = True)
    your_email = models.EmailField(max_length = 128, null = True)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    org_details = models.CharField(max_length=64, null= True)
    your_requirement = models.CharField(max_length=64, null = True)

    

CATEGORY_CHOICES = (
    ('3 Months', '3 Months'),
    ('6 Months', '6 Months'),
    ('9 Months', '9 Months'),
    ('1 Year', '1 Year'),

)
class SalesQuoteDetails(models.Model):
    enquiry = models.ForeignKey(EnquiryDetails,on_delete=models.CASCADE)
    sales_quote_id = models.CharField(max_length=64, null = True)
    product_name = models.CharField(max_length=264, null = True)
    product_id = models.CharField(max_length = 128, null = True)
    qty= models.IntegerField(null = True) 
    product_details = models.CharField(max_length = 128, null = True)
    time_period = models.CharField(choices=CATEGORY_CHOICES, max_length = 200, null = True, default="Other")
    pricing = models.CharField(max_length=64, null = True)
    added_to_cart = models.BooleanField(default=False)
    sq_reject= models.BooleanField(default=False)

class CartDetails(models.Model):
    enquiry = models.ForeignKey(EnquiryDetails,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sq_details = models.ForeignKey(SalesQuoteDetails,on_delete=models.CASCADE)
    time_period = models.CharField(choices=CATEGORY_CHOICES, max_length = 200, null = True, default="Other")
    pricing = models.CharField(max_length=64, null = True)
    qty= models.IntegerField( null = True)
    is_paid=models.BooleanField(default=False)
    total_amount=models.IntegerField( null = True)


class CompleteDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enquiry = models.ForeignKey(EnquiryDetails,on_delete=models.CASCADE)
    salesquote= models.ForeignKey(SalesQuoteDetails,on_delete=models.CASCADE)




