from django.db import models
from accounts import models as accounts_models
from django.utils import timezone

# Create your models here.

class Letter(models.Model):
    class Meta:
        db_table = 'letter'

    letterId = models.AutoField(primary_key=True)
    senderId = models.ForeignKey(accounts_models.Member, null=True, on_delete=models.SET_NULL, db_column='senderId') #acounts.member 테이블과 연결된 외래키
    content = models.CharField(max_length=10000, db_column='content')
    sendDate = models.DateTimeField(auto_now_add=True, db_column='sendDate')  # Field name made lowercase.
    receiveDate = models.DateTimeField(db_column='receiveDate')  # Field name made lowercase.
    emotion=models.IntegerField(null=True)

    #letter테이블의 발신일 표시 코드인데 없어도 될듯
    # 발신일 표시
    def send(self):
        self.sendDate=timezone.now() #발신 시간
        self.save()


class Receiveletter(models.Model):
    class Meta:
        db_table = 'receiveletter'

    receiveCol = models.AutoField(primary_key=True)  # Field name made lowercase.
    letterId = models.ForeignKey(Letter, null=True, on_delete=models.SET_NULL, db_column='letterId') #letter 테이블과 연결된 외래키
    receiverId = models.OneToOneField(accounts_models.Member, null=True, on_delete=models.SET_NULL, db_column='receiverid')
    readCheck = models.IntegerField(db_column='readCheck')  # Field name made lowercase.

    