from django.db.models import EmailField
from django.core.exceptions import ValidationError


class EMDEmailField(EmailField):
    pass


class CDNEmailField(EmailField):
    pass