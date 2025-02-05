from django.shortcuts import render,redirect
from account.forms import UserForm,PasswordResetForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_email,send_reset_password_email
from account.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import SetPasswordForm

def Home(request):
  return render(request,'account/home.html')

def Registration(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    print(form)
    if form.is_valid():
      password=form.cleaned_data.get('password')
      confirm_password=form.cleaned_data.get('confirm_password')
      if not password==confirm_password:
        messages.error(request,'Password did not match !')
        return redirect('registration')
      print("helloppppppppppppp")
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password'])
      user.is_active=False
      user.save()
      uid64 = urlsafe_base64_encode(force_bytes(user.pk))
      token = default_token_generator.make_token(user)
      activation_link = reverse('activate',kwargs={'uid64':uid64, 'token':token})
      activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
      send_activation_email(user.email,activation_url)

      messages.success(request,'Registered successfully!')
      return redirect('login')

    
  else:
   form = UserForm()

  return render(request,'account/registration.html',{'form':form})

def activate_account(request,uid64,token):
  try:
    uid = force_str(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    if user.is_active:
      messages.warning(request,'This account is already has been activated!')
      return redirect('login')
    
    if default_token_generator.check_token(user,token):
      user.is_active=True
      user.save()
      messages.success(request,'This account has been activated successfully!')
      return redirect('login')
    
    else:
      messages.error(request,'This activaton link is invalid or has been expired!')
      return redirect('login')
      
  except(TypeError,ValueError,OverflowError,User.DoesNotExist):
    messages.error(request,'Invalid activation link!')
    return redirect('login')
    pass

def Login(request):
  if request.user.is_authenticated:
    if request.user.is_seller:
      return redirect('seller-dashboard')
    
    elif request.user.is_customer:
      return redirect('customer-dashboard')
    else:
      return redirect('home')
  
  if request.method=='POST':
    email = request.POST.get('email')
    print(email)
    password  = request.POST.get('password')
    if not email or not password:
      print(password)
      messages.error(request,'Both fields are required!')
      return redirect('login')
    try:
      user = User.objects.get(email=email)
      print(user.email)
    except User.DoesNotExist:
      messages.error(request,'Invalid user or password!')
      return redirect('login')
    if not user.is_active:
      messages.error(request,'This account is not active , Please activate account   then login again !')
      return redirect('login')
    user = authenticate(request, email=email, password=password)
    if user is not None:
      print(user)
      login(request,user)
      if request.user.is_seller:
        return redirect('seller-dashboard')
    
      elif request.user.is_customer:
        return redirect('customer-dashboard')
      else:
        messages.error(request,'Permission denied!')
        return redirect('home')
    else:
      print(user)

      messages.error(request,'Invalid user or Password !')
      return redirect('login')
    
  return render(request,'account/login.html')



def Password_reset(request):
  if request.method=='POST':
    print('hello')
    form = PasswordResetForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data.get('email')
      user = User.objects.filter(email=email).first()
      if user:
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = reverse(
          'password_reset_confirm',
          kwargs={'uidb64':uidb64 ,'token':token}
        )
        absolute_reset_url=f"{request.build_absolute_uri(reset_url)}"
        send_reset_password_email(user.email,absolute_reset_url )
        
        messages.success(request,'Reset Link sent successfully!')
        return redirect('login')


  else:
    print('apple')
    form = PasswordResetForm()
  return render(request,'account/password_reset.html',{'form':form})

def password_reset_confirm(request,uidb64,token):
  try:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk = uid)
    print(user.email)
    if not default_token_generator.check_token(user,token):
      messages.error(request,'This link has been expired or Invalid!')
      return redirect('password_reset')
    if request.method=='POST':
      print(request.method)
      form = SetPasswordForm(user,request.POST)
      if form.is_valid():
        form.save()
        messages.success(request,'Password Reset successfully!')
        return redirect('login')
      else:
        for field, errors in form.errors.items():
          for error in errors:
            messages.error(request,error)

    else:
      form = SetPasswordForm(user)
    return render(request,'account/password_reset_confirm.html',{'form':form,'uidb64':uidb64, 'token':token})

  except(TypeError,ValueError,OverflowError,User.DoesNotExist):
    messages.error(request,'An error occured . Please try later')
    return redirect('password_reset')  

