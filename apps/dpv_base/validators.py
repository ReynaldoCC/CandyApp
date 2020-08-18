from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class EDNEmailValidator(EmailValidator):
    pass


class PDNEmailValidator(EmailValidator):
    pass
