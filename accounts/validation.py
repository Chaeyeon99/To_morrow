import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_phone(value):
    phone_reg = r'^([0-9]{3})-([0-9]{4})-([0-9]{4})$'
    regex = re.compile(phone_reg)

    if not regex.match(value):
        raise ValidationError(
            _('010-0000-0000 형식으로 입력해주세요.')
        )


def validate_password(password): ## 비밀번호 검증 메소드
    validate_condition = [
        lambda s: all(x.islower() or x.isupper() or x.isdigit() or (x in ['!', '@', '#', '$', '%', '^', '&', '*', '_']) for x in s), ## 영문자 대소문자, 숫자, 특수문자(리스트)만 허용
        lambda s: any(x.islower() or x.isupper() for x in s), ## 영어 대소문자 필수
        lambda s: len(s) == len(s.replace(" ","")),
        lambda s: len(s) >= 8, ## 글자수 제한
        lambda s: len(s) <= 20, ## 글자수 제한
    ]

    for validator in validate_condition:
        if not validator(password):
            return True