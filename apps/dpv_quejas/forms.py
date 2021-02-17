from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from apps.dpv_persona.forms import PersonaNaturalForm, PersonaJuridicaForm
from apps.dpv_nomencladores.forms import TelefonoForm, EmailForm, OrganismoForm, OrganizationForm, PrensaEscritaForm, \
    AnonimoForm
from apps.dpv_nomencladores.utils import is_database_synchronized

from .models import *


class QuejaForm(forms.ModelForm):
    same_address = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-check-input switch-input"}),
                                      required=False,
                                      label=_("Usar la misma dirección del dmanificado"),
                                      help_text=_("Marque aquí para asignarle a la queja la misma dirección del damnificado"))

    class Meta:
        model = Queja
        fields = (
                  'procedencia',
                  'damnificado',
                  'same_address',
                  'dir_municipio',
                  'dir_cpopular',
                  'dir_calle',
                  'dir_num',
                  'dir_entrecalle1',
                  'dir_entrecalle2',
                  'referencia',
                  'no_procendencia',
                  'no_radicacion',
                  'tipo',
                  'asunto',
                  'asunto_texto',
                  'texto',
                  'document',
        )
        widgets = {
            'dir_num': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'dir_calle': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
            'dir_entrecalle1': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
            'dir_entrecalle2': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
            'procedencia': forms.Select(attrs={"placeholder": "Seleccione una Procedencia.", "class": "form-control"}),
            'damnificado': forms.Select(attrs={"placeholder": "Seleccione un Damnificado.", "class": "form-control"}),
            'dir_municipio': forms.Select(attrs={"placeholder": "Seleccione un Municipio.", "class": "form-control"}),
            'dir_cpopular': forms.Select(attrs={"placeholder": "Seleccione un Consejo Popular.", "class": "form-control"}),
            'referencia': forms.TextInput(attrs={"placeholder": "No. referencia", "class": "form-control"}),
            'texto': forms.Textarea(attrs={"placeholder": "Cuerpo de la Queja", "class": "form-control", "rows": "6"}),
            'asunto': forms.Select(attrs={"placeholder": "Seleccione un Asunto", "class": "form-control"}),
            'tipo': forms.Select(attrs={"placeholder": "Seleccione un Tipo", "class": "form-control"}),
            'asunto_texto': forms.TextInput(attrs={"placeholder": "Asunto", "class": "form-control"}),
            'no_procendencia': forms.TextInput(attrs={"placeholder": "No. de procedencia", "class": "form-control"}),
            'no_radicacion': forms.TextInput(attrs={"placeholder": "No. de radicación", "class": "form-control"}),
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
                  'dpto', 'observaciones',
                  )
        widgets = {
            'dpto': forms.Select(attrs={"placeholder": "Seleccione un Departamento.", "class": "form-control select2"}),
            'observaciones': forms.Textarea(attrs={"placeholder": "Observasiones", "class":"form-control mtext"}),
        }


class AsignaQuejaTecnicoForm(forms.ModelForm):

    class Meta:
        model = AsignaQuejaTecnico
        fields = (
                  'tecnico', 'observaciones',
                  )
        widgets = {
            'tecnico': forms.Select(attrs={"placeholder":"Seleccionar Técnico", "class": "form-control select2"}),
            'observaciones': forms.Textarea(attrs={"placeholder": "Observasiones", "class": "form-control mtext"}),
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


class QAnonimoForm(AnonimoForm):

    def is_valid(self):
        super(QAnonimoForm, self).is_valid()
        return True

    def save(self, commit=True):
        a = Anonimo()
        a.save()
        return a


class QRespuestaForm(forms.ModelForm):

    class Meta:
        model = RespuestaQueja
        fields = ["gestion", "nivel_solucion", "conclusion_caso", "clasificacion", "texto", ]
        widgets = {
            "gestion": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "texto": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
            "nivel_solucion": forms.Select(attrs={"class": "form-control"}),
            "conclusion_caso": forms.Select(attrs={"class": "form-control"}),
            "clasificacion": forms.Select(attrs={"class": "form-control"}),
        }


class DamnificadoForm(forms.ModelForm):

    class Meta:
        model = Damnificado
        fields = "__all__"


if is_database_synchronized():
    person_queryset = PersonaNatural.objects.exclude(perfil_datos__datos_usuario__is_superuser=True)\
        .exclude(id__in=Procedencia.objects.filter(
        tipo_contenido=ContentType.objects.get_for_model(PersonaNatural)).values_list('id_objecto'))
    entity_queryset = PersonaJuridica.objects.exclude(id__in=Procedencia.objects.filter(
        tipo_contenido=ContentType.objects.get_for_model(PersonaJuridica)).values_list('id_objecto'))
else:
    person_queryset = None
    entity_queryset = None


class DamnificadoAddForm(forms.ModelForm):
    personas = forms.ModelChoiceField(queryset=person_queryset,
                                      label=_('Personas'),
                                      required=False,
                                      widget=forms.Select(attrs={'placeholder': 'Seleccionar una persona',
                                                                 'class': 'form-control'}))
    empresas = forms.ModelChoiceField(queryset=entity_queryset,
                                      label=_('Entidades'),
                                      required=False,
                                      widget=forms.Select(attrs={'placeholder': 'Seleccionar una entidad',
                                                                 'class': 'form-control'}))

    class Meta:
        model = Damnificado
        fields = [
                  'tipo_contenido',
                  'empresas',
                  'personas', ]
        widgets = {
            'tipo_contenido': forms.Select(attrs={'placeholder': 'Seleccione', 'class': 'form-control'}),
        }
