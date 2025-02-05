from django.urls import path
from customer.views import Dashboard,Password_change
urlpatterns=[
  path('dashboard/',Dashboard,name="customer-dashboard"),
  path('password_change/',Password_change,name="password_change"),

]