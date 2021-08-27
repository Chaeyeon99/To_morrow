from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages_constants
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from .forms import UserCreationForm, CustomUserChangeForm, LoginForm, PasswordForm
from .models import Member



def Index (request):
    return render(request,'accounts/Index.html',None) 


def signup(request): 
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()             
            return HttpResponseRedirect('/accounts')
        else:
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})



def login_view(request): 
    if request.user.is_authenticated:
        return HttpResponseRedirect((reverse('accounts:Index')))

    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)

        if form.is_valid():
            login_memberId = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']
            member = Member.objects.get(memberId=login_memberId)
        
            if check_password(raw_password, member.password):
                memberId = authenticate(username=login_memberId, password=raw_password)
                login(request, memberId) 
                request.session['user']=member.memberId
                return HttpResponseRedirect((reverse('letter:letterFrmMe')))

    if request.method == 'GET':
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})



@login_required
def logout_view(request):
    try : 
        if request.session.get('user'):
            del(request.session['user'])
            logout(request)
            return HttpResponseRedirect('/accounts')
    except : 
        messages.error(request, 'Error! Try Again')




@login_required
def profile(request):
    job_dictionary = { 'educaiton' : '교육자', 'student' : '학생', 'business' : '자영업자',
    'medical' : '의료직', 'artist' : '예술인', 'sports' : '운동인', 'office' : '직장인', 'finance' : '금융',
    'IT' : 'IT', 'architect' : '건설', 'public' : '공무원', 'jobseeker' : '취준생', 'housewife' : '주부',
    'soldier' : '군인', 'etc' : '기타'
    }
    if not request.session.get('user'): 
        return redirect('/accounts/login')
        
    if request.method =='GET':
        try:
            memberId=request.session.get('user')
                   
            if Member.objects.filter(memberId=memberId).exists() :
                member = Member.objects.get(memberId=memberId)
                name = member.name

                if Member.objects.filter(name=name).exists(): 
                    member=Member.objects.get(name=name)
                    member.job = job_dictionary[member.job]

                    context={ 'member' : member, 'name': name }

        except member.DoesNotExist: 
                raise Http404("member does not exist")

        return render(request, 'accounts/profile.html',context)  


@login_required
def updateProfile(request):
    if not request.session.get('user'): 
        return redirect('/accounts/login')

    if request.method == 'POST': 
        update_form = CustomUserChangeForm(request.POST, instance=request.user)
        memberId=request.session.get('user')
   
        if update_form.is_valid():    
            email = update_form.cleaned_data['email']
                    
            if Member.objects.filter(memberId=memberId).exists() :
                member = Member.objects.get(memberId=memberId)
                member.email = email
                member.save()

            update_form.save()
            MESSAGE_LEVEL = messages_constants.SUCCESS
            messages.add_message(request, messages.INFO, '정보 수정에 성공했습니다.')
            return HttpResponseRedirect('/accounts/profile', request.user.memberId)
        else:
            messages.error(request, 'Error! Try Again')
            return render(request, 'accounts/update.html', {'update_form': update_form})
    
    else :
        update_form = CustomUserChangeForm(instance = request.user)
        context = { 'update_form' : update_form   }
        return render(request, 'accounts/update.html', context) 


@login_required
def password(request):
    if request.method == "POST":
        password_change_form = PasswordForm(request.user, request.POST)
        
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.INFO, '비밀번호 변경에 성공했습니다.')
            return redirect('/letter/letterFrmMe', request.user.memberId)
        else: 
            messages.error(request, '비밀번호 변경에 실패했습니다. 다시 시도해주세요')
            return redirect('/accounts/password', request.user.memberId)
    else:
        password_change_form = PasswordForm(request.user)
        context = {
            'password_change_form': password_change_form
        }
        
        return render(request, 'accounts/password.html', context)