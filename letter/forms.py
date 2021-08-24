from django import forms
from django.forms.widgets import DateInput
from letter.models import Letter, Receiveletter
import datetime
import datetime


class TimeInput(forms.TimeInput):
    input_type = 'time'
    
class DateInput(forms.DateInput):
    input_type = 'date'


class NameForm(forms.Form):
    letter = forms.CharField(widget=forms.Textarea)


# 나에게 쓰는 편지 폼 
class WriteForm(forms.ModelForm):
    
    content = forms.CharField(widget=forms.Textarea)
    receiveDate = forms.DateTimeField(widget=DateInput())
    receiveTime = forms.TimeField(widget=TimeInput())

    class Meta:
        model=Letter
        fields=[
            'content',
            'receiveDate',
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content', '')
        receiveDate = cleaned_data.get('receiveDate', '')
        receiveTime = cleaned_data.get('receiveTime', '')
        receiveDate = datetime.datetime.combine(receiveDate, receiveTime)

       
        if content == '':
            self.add_error('content', '편지 내용을 입력하세요.')
        else:
            self.content = content

            self.receiveDate = receiveDate


# 타인에게 쓰는 편지 폼 
class WriteFormOthers(forms.ModelForm): # WriteForm_toOthers -> WriteFormOthers

    job_Choices=(('education', '교육자'), ('student', '학생'), ('business', '자영업자'), ('medical', '의료직')
    , ('artist', '예술인'), ('sports', '운동인'), ('office', '직장인'), ('finance', '금융'), ('IT', 'IT')
    , ('architect', '건설'), ('public', '공무원'), ('jobseeker', '취준생'), ('housewife', '주부')
    , ('soldier', '군인'), ('etc', '기타'))

    content = forms.CharField(widget=forms.Textarea)
    receiverGroup = forms.MultipleChoiceField(
        required = True,
        widget = forms.CheckboxSelectMultiple,
        choices = job_Choices,
    )
    receiveDate = forms.DateTimeField(widget=DateInput())
    receiveTime = forms.TimeField(widget=TimeInput())


    class Meta:
        model = Letter
        fields = [
            'content',
            'receiverGroup',
            'receiveDate',
        ]
    
    def clean(self):
        cleaned_data = super().clean()

        content = cleaned_data.get('content', '')
        receiveDate = cleaned_data.get('receiveDate', '')
        receiveTime = cleaned_data.get('receiveTime', '')
        receiveDate = datetime.datetime.combine(receiveDate, receiveTime)
        receiverGroup = cleaned_data.get('receiverGroup', '') 
       
        if content == '':
            self.add_error('content', '편지 내용을 입력하세요.')
        else:
            self.content = content
            self.receiverGroup = receiverGroup
            self.receiveDate = receiveDate

