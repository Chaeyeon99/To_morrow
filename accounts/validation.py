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