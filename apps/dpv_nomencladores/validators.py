from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


# Messages
message_on = _("Este campo solo puede contener números")
message_ol = _("Este campo solo puede contener letras")
message_nn = _("Este campo no puede contener números")
message_nl = _("Este campo no puede contener letras")
message_nsc = _("Este campos no puede contener caracteres especiales, ejem. '@', '#', '!', '.', '%', ")

# Validators
only_numbers = RegexValidator('^[0-9]*[0-9]$', message=message_on)
only_letters = RegexValidator('^[a-zA-Z ]*[a-zA-Z ]$', message=message_ol)
not_numbers = RegexValidator('[a-zA-Z ,.:;!@#$%^&*()_+-={}[]\|~`]', message=message_nn)
not_letters = RegexValidator('[0-9 ,.:;!@#$%^&*()_+-={}[]\|~`]', message=message_nl)
not_special_char = RegexValidator('[a-zA-Z0-9 ]', message=message_nsc)


'''from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

class MinimumLengthValidator(object):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("This password must contain at least %(min_length)d characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters."
            % {'min_length': self.min_length}
        )

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )
     
'''