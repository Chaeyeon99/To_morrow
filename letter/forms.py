from django import forms
from django.forms.widgets import DateInput
from letter.models import Letter, Receiveletter
import datetime

class NameForm(forms.Form):
    letter = forms.CharField(widget=forms.Textarea)


#실제 사용자에게 입력받는 정보
class WriteForm(forms.ModelForm):
    
    content = forms.CharField(widget=forms.Textarea)
    receiveDate = forms.DateTimeField()
    #receiverId=forms.

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

       
        if content == '':
            self.add_error('content', '편지 내용을 입력하세요.')
        else:
            self.content = content

            self.receiveDate = receiveDate


