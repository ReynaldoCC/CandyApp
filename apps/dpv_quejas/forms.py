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
                                              label=_("El damnificado no está en la lista"),
                                              help_text=_("Marque aqui si la persona que busca no está en la lista y se le mostrará un formulario para ingresar sus datos"))

    class Meta:
        model = Queja
        fields = ('asunto',
                  'dir_calle',
                  'dir_num',
                  'dir_entrecalle1',
                  'dir_entrecalle2',
                  'dir_municipio',
                  'dir_cpopular',
                  'procedencia',
                  'referencia',
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
            'referencia': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'texto': forms.Textarea(attrs={"placeholder": "Nombre", "class": "form-control"}),
            'asunto': forms.Select(attrs={"placeholder": "Seleccione un Asunto", "class": "form-control"}),
            'damnificado': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
        }

    def clean(self):
        if self.cleaned_data.get('dir_calle') == self.cleaned_data.get('dir_entrecalle1'):
            raise ValidationError({'dir_entrecalle1': _('La primera entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('dir_entrecalle2') == self.cleaned_data.get('dir_calle'):
            raise ValidationError({'dir_entrecalle2': _('La segunda entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('dir_entrecalle1') == self.cleaned_data.get('dir_entrecalle2'):
            raise ValidationError({'dir_entrecalle2': _('Ambas entre calles no pueden ser iguales.')})
        return  super(forms.ModelForm, self).clean()


class AsignaQuejaDptoForm(forms.ModelForm):

    class Meta:
        model = AsignaQuejaDpto
        fields = (
                  'dpto',
                  )
        widgets = {
            'dpto': forms.Select(attrs={"placeholder": "Seleccione un Departamento.", "class": "form-control select2"}),
        }


class AsignaQuejaTecnicoForm(forms.ModelForm):

    class Meta:
        model = AsignaQuejaTecnico
        fields = (
                  'tecnico',
                  )
        widgets = {
            'tecnico': forms.Select(attrs={"placeholder": "Seleccione un Técnico.", "class": "form-control select2"}),
        }


class QPersonaNaturalForm(PersonaNaturalForm):

    def __init__(self, *args, **kwargs):
        super(QPersonaNaturalForm, self).__init__(*args, **kwargs)
        self.fields['ci'].widget.attrs.update({'id': 'id_qci', 'class': 'form-control verify'})
        self.fields['nombre'].widget.attrs.update({'id': 'id_qnombre', 'class': 'form-control verify'})
        self.fields['apellidos'].widget.attrs.update({'id': 'id_qapellidos', 'class': 'form-control verify'})
        self.fields['email_address'].widget.attrs.update({'id': 'id_qemail_address', 'class': 'form-control verify'})
        self.fields['telefono'].widget.attrs.update({'id': 'id_qtelefono', 'class': 'form-control verify'})
        self.fields['movil'].widget.attrs.update({'id': 'id_qmovil', 'class': 'form-control verify'})
        self.fields['direccion_calle'].widget.attrs.update({'id': 'id_qdireccion_calle', 'class': 'form-control verify'})
        self.fields['direccion_numero'].widget.attrs.update({'id': 'id_qdireccion_numero', 'class': 'form-control verify'})
        self.fields['direccion_entrecalle1'].widget.attrs.update({'id': 'id_qdireccion_entrecalle1', 'class': 'form-control verify'})
        self.fields['direccion_entrecalle2'].widget.attrs.update({'id': 'id_qdireccion_entrecalle2', 'class': 'form-control verify'})
        self.fields['municipio'].widget.attrs.update({'id': 'id_qmunicipio', 'class': 'form-control verify'})
        self.fields['cpopular'].widget.attrs.update({'id': 'id_qcpopular', 'class': 'form-control'})
        self.fields['genero'].widget.attrs.update({'id': 'id_qgenero', 'class': 'form-control'})


class AQPersonaNaturalForm(PersonaNaturalForm):

    def __init__(self, *args, **kwargs):
        super(AQPersonaNaturalForm, self).__init__(*args, **kwargs)
        self.fields['ci'].widget.attrs.update({'id': 'id_aqci', 'class': 'form-control verify'})
        self.fields['nombre'].widget.attrs.update({'id': 'id_aqnombre', 'class': 'form-control verify'})
        self.fields['apellidos'].widget.attrs.update({'id': 'id_aqapellidos', 'class': 'form-control verify'})
        self.fields['email_address'].widget.attrs.update({'id': 'id_aqemail_address', 'class': 'form-control verify'})
        self.fields['telefono'].widget.attrs.update({'id': 'id_aqtelefono', 'class': 'form-control verify'})
        self.fields['movil'].widget.attrs.update({'id': 'id_aqmovil', 'class': 'form-control verify'})
        self.fields['direccion_calle'].widget.attrs.update({'id': 'id_aqdireccion_calle', 'class': 'form-control verify'})
        self.fields['direccion_numero'].widget.attrs.update({'id': 'id_aqdireccion_numero', 'class': 'form-control verify'})
        self.fields['direccion_entrecalle1'].widget.attrs.update({'id': 'id_aqdireccion_entrecalle1', 'class': 'form-control verify'})
        self.fields['direccion_entrecalle2'].widget.attrs.update({'id': 'id_aqdireccion_entrecalle2', 'class': 'form-control verify'})
        self.fields['municipio'].widget.attrs.update({'id': 'id_aqmunicipio', 'class': 'form-control verify'})
        self.fields['cpopular'].widget.attrs.update({'id': 'id_aqcpopular', 'class': 'form-control'})
        self.fields['genero'].widget.attrs.update({'id': 'id_aqgenero', 'class': 'form-control'})


class QPersonaJuridicaForm(PersonaJuridicaForm):

    def __init__(self, *args, **kwargs):
        super(QPersonaJuridicaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'id': 'id_pj_nombre', 'class': 'form-control verify'})
        self.fields['sigla'].widget.attrs.update({'id': 'id_pj_sigla', 'class': 'form-control verify'})
        self.fields['telefono'].widget.attrs.update({'id': 'id_pj_telefono', 'class': 'form-control verify'})
        self.fields['movil'].widget.attrs.update({'id': 'id_pj_movil', 'class': 'form-control verify'})
        self.fields['nombre_contacto'].widget.attrs.update({'id': 'id_pj_nombre_contacto', 'class': 'form-control verify'})
        self.fields['email_address'].widget.attrs.update({'id': 'id_pj_email_address', 'class': 'form-control verify'})
        self.fields['direccion_calle'].widget.attrs.update({'id': 'id_pj_direccion_calle', 'class': 'form-control verify'})
        self.fields['direccion_numero'].widget.attrs.update({'id': 'id_pj_direccion_numero', 'class': 'form-control verify'})
        self.fields['direccion_entrecalle1'].widget.attrs.update({'id': 'id_pj_direccion_entrecalle1', 'class': 'form-control verify'})
        self.fields['direccion_entrecalle2'].widget.attrs.update({'id': 'id_pj_direccion_entrecalle2', 'class': 'form-control verify'})
        self.fields['municipio'].widget.attrs.update({'id': 'id_pj_municipio', 'class': 'form-control verify'})
        self.fields['codigo_nit'].widget.attrs.update({'id': 'id_pj_codigo_nit', 'class': 'form-control verify'})
        self.fields['codigo_reuup'].widget.attrs.update({'id': 'id_pj_codigo_reuup', 'class': 'form-control verify'})


class QTelefonoForm(TelefonoForm):

    def __init__(self, *args, **kwargs):
        super(QTelefonoForm, self).__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs.update({'id': 'id_tel_numero', 'class': 'form-control verify'})


class QEmailForm(EmailForm):

    def __init__(self, *args, **kwargs):
        super(QEmailForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'id': 'id_email_email', 'class': 'form-control verify'})


class QOrganismoForm(OrganismoForm):

    def __init__(self, *args, **kwargs):
        super(QOrganismoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'id': 'id_organismo_nombre', 'class': 'form-control verify'})


class QOrganizationForm(OrganizationForm):

    def __init__(self, *args, **kwargs):
        super(QOrganizationForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'id': 'id_organizacion_nombre', 'class': 'form-control verify'})


class QPrensaEscritaForm(PrensaEscritaForm):

    def __init__(self, *args, **kwargs):
        super(QPrensaEscritaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'id': 'id_pe_nombre', 'class': 'form-control verify'})


class QGobiernoForm(GobiernoForm):

    def __init__(self, *args, **kwargs):
        super(QGobiernoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'id': 'id_gob_nombre', 'class': 'form-control verify'})
