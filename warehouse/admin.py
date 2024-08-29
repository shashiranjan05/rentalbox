from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import EnquiryDetails, SalesQuoteDetails, CompleteDetails


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','role' ,'is_staff', 'is_active',)
    list_filter = ('email','role', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)



# Register your models here.
admin.site.register(EnquiryDetails)
admin.site.register(SalesQuoteDetails)
admin.site.register(CompleteDetails)

admin.site.register(CustomUser, CustomUserAdmin)