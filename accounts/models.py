from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin 
)


class MemberManager(BaseUserManager):

    # use_in_migrations = True

    # 유저 생성 
    def create_user(self, memberId, name, birth, nickname, job, phone, email, password=None):
    
        if not memberId:
            raise ValueError('Users must have an id')

        user = self.model(
            memberId=memberId,
            name=name,
            birth=birth,
            nickname=nickname,
            job=job,
            phone=phone,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    #관리자 생성 
    def create_superuser(self, memberId, name, birth, nickname, job, phone, email, password=None):

        user = self.model(
            memberId=memberId,
            name=name,
            birth=birth,
            nickname=nickname,
            job=job,
            phone=phone,
            email=self.normalize_email(email),
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser, PermissionsMixin):

    class Meta:
        db_table = 'member'
    # objects = MemberManager()

    memberId = models.CharField(db_column='memberId', primary_key=True, max_length=50)  # Field name made lowercase.
    name = models.CharField(max_length=50)
    birth = models.DateField()
    nickname = models.CharField(unique=True, max_length=255)
    job = models.CharField(max_length=50)  # Field name made lowercase.
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)


    objects = MemberManager()
    USERNAME_FIELD = 'memberId' # 로그인시 id로 사용되는 필드 지정. 
    REQUIRED_FIELDS = ['password', 'name','birth','nickname','job', 'phone', 'email'] #필수로 입력 받을 값 


    def __str__(self):
        return self.memberId

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


