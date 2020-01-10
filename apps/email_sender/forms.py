from django import forms
from django.core.validators import EmailValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from .models import EmailConfigurate


class EmailForm(forms.Form):
    from_email = forms.CharField(max_length=255, label="From", validators=[EmailValidator, MaxLengthValidator(255)])
    cc_email = forms.CharField(max_length=511, label="CC")
    bcc_email = forms.CharField(max_length=511, label="BCC")
    recipients_email = forms.CharField(max_length=756, label="To")
    subject_email = forms.CharField(max_length=200, label="Asunto")
    body_email = forms.CharField(max_length=1000, label="Mensaje", widget=(forms.Textarea(attrs={"class": ""})))


class ContactForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(max_length=1000, label="Mensaje", widget=(forms.Textarea(attrs={"class": ""})))


class ConfigureMailForm(forms.ModelForm):

    class Meta:
        model = EmailConfigurate
        fields = ('servidor', 'puerto', 'usuario', 'password', 'use_tls', 'use_ssl', )
        widgets = {
            'puerto': forms.TextInput(attrs={"placeholder": "Puerto ej: 25", "class": "form-control"}),
            'servidor': forms.TextInput(attrs={"placeholder": "Servidor ej: localhost", "class": "form-control"}),
            'usuario': forms.TextInput(attrs={"placeholder": "Usuario", "class": "form-control"}),
            'password': forms.PasswordInput(attrs={"placeholder": "Contraseña", "class": "form-control"}),
            'use_tls': forms.CheckboxInput(attrs={"placeholder": "Contraseña", "class": "form-check-input", "type": "radio", "value": "option2", "onchange":"desmarcar_otros('id_use_tls')"}),
            'use_ssl': forms.CheckboxInput(attrs={"placeholder": "Contraseña", "class": "form-check-input", "type": "radio", "value": "option3", "onchange":"desmarcar_otros('id_use_ssl')"}),
        }

    def clean_use_tls(self):
        if self.cleaned_data.get('use_tls') == True and self.data.get('use_ssl') == True:
            raise ValidationError('No puede tener activado el TLS al mismo tiempo que el SSL')
        return self.cleaned_data.get('use_tls')

    def clean_use_ssl(self):
        if self.cleaned_data.get('use_ssl') == True and self.data.get('use_tls') == True:
            raise ValidationError('No puede tener activado el SSL al mismo tiempo que el TLS')
        return self.cleaned_data.get('use_ssl')