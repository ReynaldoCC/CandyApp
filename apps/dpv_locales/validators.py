from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import datetime

# Messages
message_aa = _("Debe seguir el patrón de XX/XX ó XX/XXXX donde se sustituyen las X por números")
message_future_year = _("El acuerdo o acta no puede ser de un año futuro.")
message_format_bad = _("El acuerdo o acta debe contener al menos y solo un slash '/' ")
message_year_bad = _("El año debe tener el siguiente formato XX ó XXXX")
message_not_number = _("El número de idenficador no puede contener letras.")
message_start_number = _("Este campo debe comenzar por un número.")


# Validators
def validate_acta_acuerdo(value):
    splited = value.split('/')
    if len(splited) is not 2:
        raise ValidationError(message=message_format_bad, code="format_bad")
    if len(splited[-1]) is not 2 and len(splited[-1]) is not 4:
        raise ValidationError(message=message_year_bad, code="year_bad")
    try:
        int(splited[-1])
    except:
        raise ValidationError(message=message_year_bad, code="year_bad")
    try:
        int(splited[0])
    except:
        raise ValidationError(message=message_not_number, code="bad_number")
    splited_year = splited[-1]
    if len(splited_year) is 2:
        splited_year = '20' + splited_year
    if int(splited_year) > datetime.date.today().year:
        raise ValidationError(message=message_future_year, code="future_year")
    return True

start_with_number = RegexValidator('^[0-9]', message=message_start_number)