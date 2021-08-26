from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput
from accounts.models import Member
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .validation import validate_phone, validate_password



class DateInput(forms.DateInput):
    input_type = 'date'

# 회원 가입 폼 
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
    validators=[validate_password])
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    validators=[validate_password])
    job_Choices=(('education', '교육자'), ('student', '학생'), ('business', '자영업자'), ('medical', '의료직')
    , ('artist', '예술인'), ('sports', '운동인'), ('office', '직장인'), ('finance', '금융'), ('IT', 'IT')
    , ('architect', '건설'), ('public', '공무원'), ('jobseeker', '취준생'), ('housewife', '주부')
    , ('soldier', '군인'), ('etc', '기타'))
    job=forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        choices=job_Choices, label="직업군"
        )
    birth = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}),label="생일")
    email = forms.EmailField(widget=(TextInput(attrs={'class': 'form-control'})),label="이메일")
    phone = forms.CharField(widget=(TextInput(attrs={'class': 'form-control'}))
    ,validators = [validate_phone], label="휴대폰번호")

    class Meta:                                                                                                     
        model = Member
        fields = ['memberId', 'name','birth','job', 'nickname','phone', 'email']
        labels = {"memberId": "ID", "name": "이름", "nickname":"닉네임",}
        widgets = {
            'memberId': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    


# 개인 정보 수정
class CustomUserChangeForm(UserChangeForm):
    password=None
    job_Choices=(('education', '교육자'), ('student', '학생'), ('business', '자영업자'), ('medical', '의료직')
    , ('artist', '예술인'), ('sports', '운동인'), ('office', '직장인'), ('finance', '금융'), ('IT', 'IT')
    , ('architect', '건설'), ('public', '공무원'), ('jobseeker', '취준생'), ('housewife', '주부')
    , ('soldier', '군인'), ('etc', '기타'))

    job=forms.ChoiceField(
        widget=forms.Select(attrs={'class':'form-control'}),
        choices=job_Choices, label="직업군"
        )
    birth = forms.DateField(widget=DateInput(attrs={'class': 'form-control'}),label="생일")
    email = forms.EmailField(widget=(TextInput(attrs={'class': 'form-control'})),label="이메일")
    phone = forms.CharField(widget=(TextInput(attrs={'class': 'form-control'}))
    ,validators = [validate_phone], label="휴대폰번호")


    class Meta:
        model = get_user_model()
        fields = ['memberId', 'name','birth','job', 'nickname','phone', 'email']
        labels = {"memberId": "ID", "name": "이름", "nickname":"닉네임",}
        widgets = {
            'memberId': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
        }

    #폼 설정 : read only
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['memberId'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True

            
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email', '')
        self.email = str(email)

class PasswordForm(PasswordChangeForm):

    old_password = forms.CharField(label='현재 비밀번호', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(label='새 비밀번호', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(label='새 비밀번호 확인', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)




class LoginForm(AuthenticationForm):
    username = forms.CharField(label='ID', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='PW', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)