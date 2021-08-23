from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .forms import addUserForm
from .models import Member


# 메인 홈 
def Index (request):
    return render(request,'accounts/Index.html',None) 

# 일반 유저 회원가입
def SignUp(request): 
    if request.method == "POST":
        form = addUserForm(request.POST)
        if form.is_valid():
            form.save() 
            memberId = form.cleaned_data.get('memberId')  
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(memberId=memberId, password=raw_password) 
            #login(request, user) 
            return HttpResponseRedirect('/accounts')
    else:
        form = addUserForm()
    return render(request, 'accounts/SignUp.html', {'form': form})