from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from apps.dpv_persona.forms import PersonaNaturalForm, PersonaJuridicaForm
from apps.dpv_nomencladores.forms import TelefonoForm, EmailForm, OrganismoForm, OrganizationForm, PrensaEscritaForm, \
    GobiernoForm
from .models import *


class QuejaForm(forms.ModelForm):
    tipo_procedencia = forms.ModelChoiceField(queryset=TipoProcedencia.objects.all(),
                                              label=_("Procedencia generica"),
                                              help_text=_("Aquí se expresa si la queja proviene de una Empresa, Persona, Organismo, Anónimo, etc.."),
                                              widget=forms.Select(attrs={"class": "form-control"}))
    damnificado_not_indb = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-check-input switch-input"}),
                                              initial=False,
                                              required=False,
                                              label=_("El damnificado no está en la lista"),
                                              help_text=_("Marque aqui si la persona que busca no está en la lista y se le mostrará un formulario para ingresar sus datos"))

    class Meta:
        model = Queja
        fields = ('asunto',
                  'asunto_texto',
                  'no_procendencia',
                  'no_radicacion',
                  'tipo',
                  'dir_calle',
                  'dir_num',
                  'dir_entrecalle1',
                  'dir_entrecalle2',
                  'dir_municipio',
                  'dir_cpopular',
                  'procedencia',
                  'referencia',
                  'responder_a',
                  'tipo_procedencia',
                  'damnificado_not_indb',
                  'texto',)
        widgets = {
            'dir_num': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'dir_calle': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
            'dir_entrecalle1': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
            'dir_entrecalle2': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
            'procedencia': forms.Select(attrs={"placeholder": "Seleccione una Procedencia.", "class": "no-show form-control"}),
            'dir_municipio': forms.Select(attrs={"placeholder": "Seleccione un Municipio.", "class": "form-control"}),
            'dir_cpopular': forms.Select(attrs={"placeholder": "Seleccione un Consejo Popular.", "class": "form-control"}),
            'referencia': forms.TextInput(attrs={"placeholder": "No. referencia", "class": "form-control"}),
            'texto': forms.Textarea(attrs={"placeholder": "Cuerpo de la Queja", "class": "form-control", "rows": "6"}),
            'asunto': forms.Select(attrs={"placeholder": "Seleccione un Asunto", "class": "form-control"}),
            'tipo': forms.Select(attrs={"placeholder": "Seleccione un Tipo", "class": "form-control"}),
            'asunto_texto': forms.TextInput(attrs={"placeholder": "Asunto", "class": "form-control"}),
            'no_procendencia': forms.TextInput(attrs={"placeholder": "No. de procedencia", "class": "form-control"}),
            'no_radicacion': forms.TextInput(attrs={"placeholder": "No. de radicación", "class": "form-control"}),
            'responder_a': forms.Select(attrs={"placeholder": "Seleccione a quien responder.", "class": "form-control"}),
        }

    def clean(self):
        if self.cleaned_data.get('dir_calle') == self.cleaned_data.get('dir_entrecalle1'):
            raise ValidationError({'dir_entrecalle1': _('La primera entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('dir_entrecalle2') == self.cleaned_data.get('dir_calle'):
            raise ValidationError({'dir_entrecalle2': _('La segunda entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('dir_entrecalle1') == self.cleaned_data.get('dir_entrecalle2'):
            raise ValidationError({'dir_entrecalle2': _('Ambas entre calles no pueden ser iguales.')})
        return super(QuejaForm, self).clean()


class AsignaQuejaDptoForm(forms.ModelForm):

    class Meta:
        model = AsignaQuejaDpto
        fields = (
                  'dpto', 'observaciones', 'rechazada',
                  )
        widgets = {
            'dpto': forms.Select(attrs={"placeholder": "Seleccione un Departamento.", "class": "form-control select2"}),
            'observaciones': forms.Textarea(attrs={"placeholder": "Observasiones", "class":"form-control mtext"}),
            'rechazada': forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class AsignaQuejaTecnicoForm(forms.ModelForm):

    class Meta:
        model = AsignaQuejaTecnico
        fields = (
                  'tecnico', 'observaciones', 'rechazada',
                  )
        widgets = {
            'tecnico': forms.Select(attrs={"placeholder": "Seleccione un Técnico.", "class": "form-control select2"}),
            'observaciones': forms.Textarea(attrs={"placeholder": "Observasiones", "class": "form-control mtext"}),
            'rechazada': forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class QPersonaNaturalForm(PersonaNaturalForm):

    def __init__(self, *args, **kwargs):
        super(QPersonaNaturalForm, self).__init__(*args, **kwargs)
        self.fields['ci'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['apellidos'].widget.attrs.update({'class': 'form-control'})
        self.fields['email_address'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['movil'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_calle'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_numero'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_entrecalle1'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_entrecalle2'].widget.attrs.update({'class': 'form-control'})
        self.fields['municipio'].widget.attrs.update({'class': 'form-control'})
        self.fields['cpopular'].widget.attrs.update({'class': 'form-control'})
        self.fields['genero'].widget.attrs.update({'class': 'form-control'})


class AQPersonaNaturalForm(PersonaNaturalForm):

    def __init__(self, *args, **kwargs):
        super(AQPersonaNaturalForm, self).__init__(*args, **kwargs)
        self.fields['ci'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['apellidos'].widget.attrs.update({'class': 'form-control'})
        self.fields['email_address'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['movil'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_calle'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_numero'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_entrecalle1'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_entrecalle2'].widget.attrs.update({'class': 'form-control'})
        self.fields['municipio'].widget.attrs.update({'class': 'form-control'})
        self.fields['cpopular'].widget.attrs.update({'class': 'form-control'})
        self.fields['genero'].widget.attrs.update({'class': 'form-control'})


class QPersonaJuridicaForm(PersonaJuridicaForm):

    def __init__(self, *args, **kwargs):
        super(QPersonaJuridicaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        self.fields['sigla'].widget.attrs.update({'class': 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class': 'form-control'})
        self.fields['movil'].widget.attrs.update({'class': 'form-control'})
        self.fields['nombre_contacto'].widget.attrs.update({'class': 'form-control'})
        self.fields['email_address'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_calle'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_numero'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_entrecalle1'].widget.attrs.update({'class': 'form-control'})
        self.fields['direccion_entrecalle2'].widget.attrs.update({'class': 'form-control'})
        self.fields['municipio'].widget.attrs.update({'class': 'form-control'})
        self.fields['cpopular'].widget.attrs.update({'class': 'form-control'})
        self.fields['codigo_nit'].widget.attrs.update({'class': 'form-control'})
        self.fields['codigo_reuup'].widget.attrs.update({'class': 'form-control'})


class QTelefonoForm(TelefonoForm):

    def __init__(self, *args, **kwargs):
        super(QTelefonoForm, self).__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs.update({'class': 'form-control',
                                                   'placeholder': 'No. de teléfono'})


class QEmailForm(EmailForm):

    def __init__(self, *args, **kwargs):
        super(QEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'dirección Email'})


class QOrganismoForm(OrganismoForm):

    def __init__(self, *args, **kwargs):
        super(QOrganismoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control',
                                                   'placeholder': 'Nombre'})


class QOrganizationForm(OrganizationForm):

    def __init__(self, *args, **kwargs):
        super(QOrganizationForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control',
                                                   'placeholder': 'Nombre'})


class QPrensaEscritaForm(PrensaEscritaForm):

    def __init__(self, *args, **kwargs):
        super(QPrensaEscritaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control',
                                                   'placeholder': 'Nombre'})
        self.fields['siglas'].widget.attrs.update({'class': 'form-control',
                                                   'placeholder': 'siglas'})


class QGobiernoForm(GobiernoForm):

    def __init__(self, *args, **kwargs):
        super(QGobiernoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'form-control',
                                                   'placeholder': 'Nombre'})


class QAnonimoForm(forms.Form):

    def is_valid(self):
        return True

    def save(self, *args, **kwargs):
        return None
