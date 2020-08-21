from django import forms
from apps.dpv_base.Widgets import DivCheckboxSelectMultiple
from .models import *


class ProvinciaForm(forms.ModelForm):

    class Meta:
        model = Provincia
        fields = ['nombre', 'numero']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control'}),
        }


class MunicipioForm(forms.ModelForm):
    calles = forms.ModelMultipleChoiceField(queryset=Calle.objects.all(),
                                            label='Calles',
                                            widget=DivCheckboxSelectMultiple(attrs={'placeholder': 'Nombre',
                                                                                     'class': 'form-control multi-select-box'}))

    class Meta:
        model = Municipio
        fields = ['numero', 'nombre', 'provincia', 'calles']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control'}),
            'provincia': forms.Select(attrs={'placeholder': 'Seleccione Provincia', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(MunicipioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.fields['calles'].initial = list(self.instance.calle_set.all())

    def save(self, *args, **kwargs):
        obj = super(MunicipioForm, self).save(*args, **kwargs)
        if self.cleaned_data.get('calles'):
            obj.calle_set.set(self.cleaned_data.get('calles'))
        return obj


class ConsejoPopularForm(forms.ModelForm):
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(),
                                       widget=forms.Select(attrs={'placeholder': 'Seleccione una provincia',
                                                                  'class': 'form-control'}))

    class Meta:
        model = ConsejoPopular
        fields = ['numero', 'nombre', 'provincia', 'municipio']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control'}),
            'municipio': forms.Select(attrs={'placeholder': 'Seleccione un Municipio', 'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(ConsejoPopularForm, self).__init__(*args, **kwargs)
        if self.instance and isinstance(self.instance, ConsejoPopular):
            if hasattr(self.instance, 'municipio') and self.instance.municipio.id:
                self.fields['provincia'].initial = self.instance.municipio.provincia


class OrganismoForm(forms.ModelForm):

    class Meta:
        model = Organismo
        fields = ['nombre', 'siglas', 'email', 'telefono', 'nombre_contacto']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'siglas': forms.TextInput(attrs={'placeholder': 'Siglas', 'class': 'form-control'}),
            'nombre_contacto': forms.TextInput(attrs={'placeholder': 'Nombre de contacto', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono', 'class': 'form-control'}),
        }


class DestinoForm(forms.ModelForm):

    class Meta:
        model = Destino
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
        }


class CalleForm(forms.ModelForm):

    class Meta:
        model = Calle
        fields = ['nombre', 'municipios']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'municipios': DivCheckboxSelectMultiple(attrs={'placeholder': 'Nombre', 'class': 'form-control multi-select-box'}),
        }


class PisoForm(forms.ModelForm):

    class Meta:
        model = Piso
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
        }


class ConceptoForm(forms.ModelForm):

    class Meta:
        model = Concepto
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
        }


class GeneroForm(forms.ModelForm):

    class Meta:
        model = Genero
        fields = ['nombre', 'sigla']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'sigla': forms.TextInput(attrs={'placeholder': 'Sigla', 'class': 'form-control'}),
        }


class CentroTrabajoForm(forms.ModelForm):

    class Meta:
        model = CentroTrabajo
        fields = ['nombre', 'numero', 'siglas', 'municipio', 'oc', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control'}),
            'siglas': forms.TextInput(attrs={'placeholder': 'Siglas', 'class': 'form-control'}),
            'municipio': forms.Select(attrs={'placeholder': 'Seleccionar Municipio', 'class': 'form-control'}),
            'oc': forms.CheckboxInput()
        }


class AreaTrabajoForm(forms.ModelForm):

    class Meta:
        model = AreaTrabajo
        fields = ['nombre', 'numero', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control'}),
        }


class CodificadorAsuntoForm(forms.ModelForm):

    class Meta:
        model = CodificadorAsunto
        fields = ['nombre', 'numero', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control'}),
        }


class TipoQuejaForm(forms.ModelForm):

    class Meta:
        model = TipoQueja
        fields = ['nombre', 'numero', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Código', 'class': 'form-control'}),
        }


class TipoProcedenciaForm(forms.ModelForm):

    class Meta:
        model = TipoProcedencia
        fields = ['nombre', 'cant_dias', 'enviar', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'enviar': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'cant_dias': forms.TextInput(attrs={'placeholder': 'Días', 'class': 'form-control'}),
        }


class ProcedenciaForm(forms.ModelForm):

    class Meta:
        model = Procedencia
        fields = ['nombre', 'tipo', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'enviar': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'tipo': forms.Select(attrs={'placeholder': 'Seleccione', 'class': 'form-control'}),
        }


class EstadoForm(forms.ModelForm):

    class Meta:
        model = Estado
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
        }


class ClasificacionRespuestaForm(forms.ModelForm):

    class Meta:
        model = ClasificacionRespuesta
        fields = ['nombre', 'codigo' ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'placeholder': 'Código', 'class': 'form-control'}),
        }


class PrensaEscritaForm(forms.ModelForm):

    class Meta:
        model = PrensaEscrita
        fields = ['nombre', 'siglas', 'nombre_contacto', 'email', 'telefono', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'siglas': forms.TextInput(attrs={'placeholder': 'Siglas', 'class': 'form-control'}),
            'nombre_contacto': forms.TextInput(attrs={'placeholder': 'Nombre de contacto', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono', 'class': 'form-control'}),
        }


class TelefonoForm(forms.ModelForm):

    class Meta:
        model = Telefono
        fields = ['numero', ]
        widgets = {
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control'}),
        }


class EmailForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = ['email']
        widgets = {
            'email': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control'}),
        }


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organizacion
        fields = ['nombre', 'siglas', 'email', 'telefono', 'nombre_contacto', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'siglas': forms.TextInput(attrs={'placeholder': 'Siglas', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono', 'class': 'form-control'}),
            'nombre_contacto': forms.TextInput(attrs={'placeholder': 'Nombre de contacto', 'class': 'form-control'}),
        }


class RespuestaAQuejaForm(forms.ModelForm):

    class Meta:
        model = RespuestaAQueja
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
        }


class AnonimoForm(forms.ModelForm):

    class Meta:
        model = Anonimo
        fields = ["name", ]


class RedSocialForm(forms.ModelForm):

    class Meta:
        model = RedSocial
        fields = ["nombre", "logo", ]
        widgets = {
            "nombre": forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            "dominio": forms.URLInput(attrs={'placeholder': 'Dominio', 'class': 'form-control'}),
            "logo": forms.FileInput(attrs={'placeholder': 'Subir un Logo', 'class': 'form-control'}),
        }


class ProcedenciaWebForm(forms.ModelForm):

    class Meta:
        model = ProcedenciaWeb
        fields = ["nombre", "perfil", "email", "red_social", ]
        widgets = {
            "nombre": forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            "perfil": forms.TextInput(attrs={'placeholder': 'Perfil', 'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'placeholder': 'Correo Electrónico', 'class': 'form-control'}),
            "red_social": forms.Select(attrs={'placeholder': 'Seleccione una Red Social', 'class': 'form-control'}),
        }
