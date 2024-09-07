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

PRODUCT_CATEGORIES = (
    ('APPLIANCES', 'APPLIANCES'),
    ('ELECTRONICS', 'ELECTRONICS'),
    ('FURNITURE', 'FURNITURE'),
   
)

# product id, product name , categories, sub-categories,product details, pricing, 

class Products(models.Model):
    sku= models.CharField(max_length=264, null = True)
    image = models.ImageField(upload_to='products/', blank=True, null=True) 
    name= models.CharField(max_length=264, null = True)
    categories = models.CharField(choices=PRODUCT_CATEGORIES, max_length = 200, null = True, default="Other")
    description= models.CharField(max_length=1264, null = True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    brand = models.CharField(max_length=100, blank=True, null=True)
    price= models.DecimalField(max_digits=25, decimal_places=2)
    is_available = models.BooleanField(default=True)  
    stock = models.PositiveIntegerField()  
    tags = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.name


class SalesQuoteDetails(models.Model):
    enquiry = models.ForeignKey(EnquiryDetails,on_delete=models.CASCADE)
    sales_quote_id = models.CharField(max_length=64, null = True)
    product_obj = models.ForeignKey(Products,on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=264, null = True)   #
    product_id = models.CharField(max_length = 128, null = True)   #
    qty= models.IntegerField(null = True)                           
    product_details = models.CharField(max_length = 128, null = True)  #
    time_period = models.CharField(choices=CATEGORY_CHOICES, max_length = 200, null = True, default="Other")
    pricing = models.CharField(max_length=64, null = True)  #
    added_to_cart = models.BooleanField(default=False)
    sq_reject= models.BooleanField(default=False)


#for adding to cart items 
class CartDetails(models.Model):
    enquiry = models.ForeignKey(EnquiryDetails,on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sq_details = models.ForeignKey(SalesQuoteDetails,on_delete=models.CASCADE, null=True)
    product_obj = models.ForeignKey(Products,on_delete=models.CASCADE, null=True)
    time_period = models.CharField(choices=CATEGORY_CHOICES, max_length = 200, null = True, default="1 Year")
    pricing = models.CharField(max_length=64, null = True)
    qty = models.IntegerField(default=1, null=True)
    is_paid=models.BooleanField(default=False)
    total_amount=models.IntegerField(null = True)


## for connecting one single cart in a user profile 
##my Order
class MyOrder(models.Model):
    cart = models.ManyToManyField(CartDetails,related_name='my_order')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)

    razor_pay_order_id = models.CharField(max_length=64, null = True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=64, null = True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=64, null = True, blank=True)



# this is not used till 
class CompleteDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enquiry = models.ForeignKey(EnquiryDetails,on_delete=models.CASCADE)
    salesquote= models.ForeignKey(SalesQuoteDetails,on_delete=models.CASCADE)




