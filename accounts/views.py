from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password


from .forms import UserCreationForm
from .models import Member


# 메인 홈 
def Index (request):
    return render(request,'accounts/Index.html',None) 

# 회원가입
def signup(request): 
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()             
            return HttpResponseRedirect('/accounts')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


#로그인
def login(request): 
    if request.user.is_authenticated:
        return HttpResponseRedirect('/accounts/Index')

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            print("cleaned_data : ", form.cleaned_data)
            memberId = form.cleaned_data['username']
            print("memberId : ", memberId)
            raw_password = form.cleaned_data['password']
            member = Member.objects.get(memberId=memberId)
            
            if check_password(raw_password, member.password):
                request.session['user']=member.memberId
                return redirect('/accounts')
            else:
                print('비밀번호를 틀렸습니다.')
    
    if request.method == 'GET':
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})
