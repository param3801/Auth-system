from django.shortcuts import render,redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from core.decorators import login_and_role_required




@login_and_role_required("customer")
def Dashboard(request):
  return render(request,'customer/dashboard.html')

@login_and_role_required("customer")
def Password_change(request):
  if request.method=='POST':
    form = PasswordChangeForm(request.user,request.POST)
    print(form)
    if form.is_valid():
      x = form.cleaned_data.get('email')
      print(x)
      form.save()
      logout(request)
      messages.success(request,'Password changed succesfully please login with new password!')
      return redirect('login')
    else:
      for field, errors in form.errors.items():
        for error in errors:
          messages.error(request,error)
  else:
    form = PasswordChangeForm(user=request.user)
  return render(request,'customer/password_change.html',{'form':form})

# Create your views here.
