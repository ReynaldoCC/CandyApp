from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator, RegexValidator
from django.utils.translation import ugettext_lazy as _, ngettext_lazy
import datetime

chars = 'qwertyuiopasdfghjklzxcvbnmñQWERTYUIOPASDFGHJKLZXCVBNMÑ'
message_bad_length = _('Asegurece que tenga solo 11 dígitos')
message_no_alpha = _('Asegurece que no tenga caracteres alfabéticos')
message_no_valid_date = _('Asegurece que los 6 primeros dígitos conformen una fecha válida')
message_future_date = _('Asegurece que la fecha del carnet de identidad no esté en el futuro')
message_not_blank = _('El Carnet de Identidad no puede estar en blanco')
message_bad_nit = _('No es un código NiT válido el mismo tiene la nomenclatura <XXXXXXXXXXX> donde cada X es un número.')
message_bad_reeup = _('No es un código Reeup válido el mismo tiene la nomenclatura <XXX.X.XXXXX> donde cada X es un número.')

def year_to_full(cadena):
    if len(cadena) != 2:
        raise ValidationError('Error en la longitud, longitud del año debe ser 2', code='bad_lenght')
    if cadena[0] in chars or cadena[1] in chars:
        raise ValidationError('El año no puede contener caracteres', code='bad_formed')
    current_year = str(datetime.datetime.today().year)[2:4]
    if int(current_year) >= int(cadena):
        cadena = str(datetime.datetime.today().year - 100)[:2] + cadena
    else:
        cadena = str(datetime.datetime.today().year)[:2] + cadena
    return cadena


def secure_date(cadena):
    param_year = cadena[:2]
    param_month = cadena[2:4]
    param_day = cadena[4:6]
    if int(param_month) > 12:
        return False
    year_to = year_to_full(param_year)
    try:
        datetime.datetime(int(year_to), int(param_month), int(param_day), 0, 0)
    except:
        return False
    return True


def ci_validate(value):
    if len(value) is 0 or value is '' or value is None:
        raise ValidationError(message=message_not_blank, code="not_blank")
    if len(value) is not 11:
        raise ValidationError(message=message_bad_length, code="bad_length")
    try:
        int(value)
    except:
        raise ValidationError(message=message_no_alpha, code="not_alpha")
    ci_date = value[:6]
    if not secure_date(ci_date):
        raise ValidationError(message=message_no_valid_date, code="not_valid_date")
    return True


validate_nit_cuba = RegexValidator('[0-9]{11}', message=message_bad_nit)
validate_reuup = RegexValidator('[0-9]{3}[.]\d[.]\d{5}', message=message_bad_reeup)