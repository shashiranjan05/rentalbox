from . import views
from django.urls import path

urlpatterns = [
    path('enquiry/', views.enquiry_view, name='enquiry'),
    path('salesquote/', views.sales_quote_view, name='sales quote form'),
    path('register/',views.register_view, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('dashboard/',views.dashboard_view, name='dashboard')
]