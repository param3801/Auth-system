from django.urls import path
from customer.views import Dashboard
urlpatterns=[
  path('seller_dashboard/',Dashboard,name="seller-dashboard"),
]