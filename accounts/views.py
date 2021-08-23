from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .forms import UserCreationForm
from .models import Member


# 메인 홈 
def Index (request):
    return render(request,'accounts/Index.html',None) 

# 일반 유저 회원가입
# def signup(request): 
#     if request.method == "POST":
#         form = addUserForm(request.POST)
#         if form.is_valid():
#             form.save() 
#             memberId = form.cleaned_data.get('memberId')  
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(memberId=memberId, password=raw_password) 
#             #login(request, user) 
#             return HttpResponseRedirect('/accounts')
#     else:
#         form = addUserForm()
#     return render(request, 'accounts/signup.html', {'form': form})


def signup(request): 
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            memberId = form.cleaned_data.get('memberId')  
            raw_password = form.cleaned_data.get('password1')
            # user = authenticate(memberId=memberId, password=raw_password) 
            #login(request, user) 
            return HttpResponseRedirect('/accounts')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


#로그인
# def login(request): 
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('/account/Index')

#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             memberId = form.cleaned_data.get('memberId')
#             raw_password = form.cleaned_data.get('password1')
#             member = authenticate(memberId=memberId, password=raw_password)
#             if member is not None:
#                 print(member)
#                 login(request, member) 
#                 return HttpResponseRedirect('/accounts')
#             else:
#                 print('User not found')
#         else:
#             return render(request, 'accounts/login.html', {'form': form})
    
#     if request.method == 'GET':
#         form = AuthenticationForm()
    
#     return render(request, 'accounts/login.html', {'form': form})
    
# def login(request):
#     username=request.POST['username']
#     password=request.POST['password']
#     Member.user=authenticate(request,username=username,password=password)
#     if Member.user is not None:
#         login(request, Member.user)
#         return HttpResponseRedirect('/accounts')
#     else:
#         return render(request, 'accounts/login.html')

#     if request.user.is_authenticated:
#         return HttpResponseRedirect('/account/Index')
#     if request.method=='POST':
#         user=authenticate(username=username, password=password)
#     if user.is_valid():
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect('/accounts')
#             else:
#                 print('User not found')
#         else:
#             return render(request, 'accounts/login.html', {'user':user})
#     if request.method =='GET':
#         user=AuthenticationForm()
#     return render(request, 'accounts/login.html', {'user': user})
