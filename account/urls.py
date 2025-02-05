from django.urls import path
from account.views import Home,Registration,Login,Password_reset,activate_account,password_reset_confirm
from django.contrib.auth.views import LogoutView
urlpatterns=[
  path('',Home,name='home'),
  path('registration/',Registration,name='registration'),
  path('activate/<str:uid64>/<str:token>/',activate_account,name="activate"),
  path('login/',Login,name='login'),
  path('logout/',LogoutView.as_view(),name="logout"),
  path('pasword_reset/',Password_reset,name='password_reset'),
  path('password_reset_confirm/<uidb64>/<token>/',password_reset_confirm,name="password_reset_confirm"),

  # path('pasword_reset_confirm/',Password_reset_confirm,name='password_reset_confirm'),

]