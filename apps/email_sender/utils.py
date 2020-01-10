from django.core.mail import EmailMessage
from django.core.validators import EmailValidator
import os
import sys


setting_file_path = os.environ.get('DJANGO_SETTINGS_MODULE')


def send_email(obj):
    em = EmailMessage()



