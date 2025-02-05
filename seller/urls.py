from django.urls import path
from seller.views import Seller_dashboard
urlpatterns=[
  path('dashboard/',Seller_dashboard,name="seller-dashboard"),
]