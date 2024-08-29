from django.contrib import admin

# Register your models here.
from .models import EnquiryDetails, SalesQuoteDetails, CompleteDetails

# Register your models here.
admin.site.register(EnquiryDetails)
admin.site.register(SalesQuoteDetails)
admin.site.register(CompleteDetails)

