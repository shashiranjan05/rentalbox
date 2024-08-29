from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User


# Create your models here.
# class User(AbstractUser):
#     is_customer = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_partner = models.BooleanField(default=False)

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
    product_name = models.CharField(max_length=264, null = True)
    product_id = models.CharField(max_length = 128, null = True)
    product_details = models.CharField(max_length = 128, null = True)
    time_period = models.CharField(choices=CATEGORY_CHOICES, max_length = 200, null = True, default="Other")
    pricing = models.CharField(max_length=64, null = True)

class CompleteDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    enquiry = models.ForeignKey(EnquiryDetails,on_delete=models.CASCADE)
    salesquote= models.ForeignKey(SalesQuoteDetails,on_delete=models.CASCADE)




