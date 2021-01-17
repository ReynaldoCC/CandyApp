from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address, RegexValidator


validate_fqdn = RegexValidator('([a-z]+[.])+[a-z]+', message="Eso no puede ser un url válido.", code="not_valid_fqdn")


def validate_ip46_fqdn_address(value):
    try:
        validate_fqdn(value)
    except ValidationError:
        try:
            validate_ipv46_address(value)
        except ValidationError:
            raise ValidationError('Introdusca un FQDN o Direccion IP valido')

