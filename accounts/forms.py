from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Member
# 회원가입 폼
class addUserForm(UserCreationForm):  
    class Meta:
        model = Member
        fields = ['memberId', 'name','birth','nickname','job', 'phone', 'email']