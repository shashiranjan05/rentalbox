from warehouse import views
from django.urls import path

urlpatterns = [
    path('enquiry/', views.enquiry_view, name='enquiry'),
    path('salesquote/', views.sales_quote_view, name='salesquote'),
    path('register/',views.register_view, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('dashboard/',views.dashboard_view, name='dashboard'),
    path('mycart/',views.cart_details_view, name='mycart'),
    path('addtocart/<int:id>',views.add_to_cart_view,name='add_to_cart'),
    path('create_order/',views.create_order,name='create_order'),
    path('sqreject/<int:id>/', views.reject_sales_quote_view, name='reject_sales_quote'),
    path('success/', views.success, name='success')
]
