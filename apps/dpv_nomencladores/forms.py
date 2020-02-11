from django import forms
from apps.dpv_base.Widgets import DivCheckboxSelectMultiple
from .models import *


class ProvinciaForm(forms.ModelForm):

    class Meta:
        model = Provincia
        fields = ['nombre', 'numero']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder':'Nombre', 'class': 'form-control malpha'}),
            'nombre': forms.TextInput(attrs={'placeholder':'Nombre', 'class': 'form-control mname'}),
            'numero': forms.TextInput(attrs={'placeholder':'Número', 'class': 'form-control mnumber'}),
        }


class MunicipioForm(forms.ModelForm):

    class Meta:
        model = Municipio
        fields = ['numero', 'nombre', 'provincia']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control mnum'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control mnumber'}),
            'provincia': forms.Select(attrs={'placeholder':'Seleccionar Provincia', 'class': 'form-control'})
        }


class ConsejoPopularForm(forms.ModelForm):

    class Meta:
        model = ConsejoPopular
        fields = ['numero', 'nombre', 'municipio']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control mnumber'}),
            'municipio': forms.Select(attrs={'placeholder':'Seleccionar Municipio', 'class': 'form-control'})
        }


class OrganismoForm(forms.ModelForm):

    class Meta:
        model = Organismo
        fields = ['nombre', 'siglas']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control mnum'}),
            'siglas': forms.TextInput(attrs={'placeholder': 'Siglas', 'class': 'form-control mnum'}),
        }


class DestinoForm(forms.ModelForm):

    class Meta:
        model = Destino
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control mnum'}),
        }


class CalleForm(forms.ModelForm):

    class Meta:
        model = Calle
        fields = ['nombre', 'municipios']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'municipios': DivCheckboxSelectMultiple(attrs={'placeholder': 'Nombre', 'class': 'form-control multi-select-box'}),
        }


class PisoForm(forms.ModelForm):

    class Meta:
        model = Piso
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control mnum'}),
        }


class ConceptoForm(forms.ModelForm):

    class Meta:
        model = Concepto
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control mname'}),
        }


class GeneroForm(forms.ModelForm):

    class Meta:
        model = Genero
        fields = ['nombre', 'sigla']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'sigla': forms.TextInput(attrs={'placeholder': 'Sigla', 'class': 'form-control mnum'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control mname'}),
            'sigla': forms.TextInput(attrs={'placeholder': 'Sigla', 'class': 'form-control mname'}),
        }


class CentroTrabajoForm(forms.ModelForm):

    class Meta:
        model = CentroTrabajo
        fields = ['nombre', 'numero', 'siglas', 'municipio', 'oc', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control mnum'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control mnumber'}),
            'siglas': forms.TextInput(attrs={'placeholder': 'Siglas', 'class': 'form-control mnum'}),
            'municipio': forms.Select(attrs={'placeholder': 'Seleccionar Municipio', 'class': 'form-control select2'}),
            'oc': forms.CheckboxInput()
        }


class AreaTrabajoForm(forms.ModelForm):

    class Meta:
        model = AreaTrabajo
        fields = ['nombre', 'numero', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control mnum'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control mnumber'}),
        }


class CodificadorAsuntoForm(forms.ModelForm):

    class Meta:
        model = CodificadorAsunto
        fields = ['nombre', 'numero', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Número', 'class': 'form-control mnumber'}),
        }


class TipoQuejaForm(forms.ModelForm):

    class Meta:
        model = TipoQueja
        fields = ['nombre', 'numero', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Código', 'class': 'form-control mname'}),
        }


class TipoProcedenciaForm(forms.ModelForm):

    class Meta:
        model = TipoProcedencia
        fields = ['nombre', 'cant_dias', 'enviar', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'enviar': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'cant_dias': forms.TextInput(attrs={'placeholder': 'Días', 'class': 'form-control mnumber'}),
        }


class ProcedenciaForm(forms.ModelForm):

    class Meta:
        model = Procedencia
        fields = ['nombre', 'tipo', ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'enviar': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'tipo': forms.Select(attrs={'placeholder': 'Seleccione', 'class': 'form-control'}),
        }


class EstadoForm(forms.ModelForm):

    class Meta:
        model = Estado
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
        }


class ClasificacionRespuestaForm(forms.ModelForm):

    class Meta:
        model = ClasificacionRespuesta
        fields = ['nombre', 'codigo' ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'codigo': forms.TextInput(attrs={'placeholder': 'Código', 'class': 'form-control mname'}),
        }


class PrensaEscritaForm(forms.ModelForm):

    class Meta:
        model = PrensaEscrita
        fields = ['nombre', 'siglas']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control malpha'}),
            'siglas': forms.TextInput(attrs={'placeholder': 'Siglas', 'class': 'form-control mname'}),
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
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
        }


class GobiernoForm(forms.ModelForm):

    class Meta:
        model = Gobierno
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
        }


class RespuestaAQuejaForm(forms.ModelForm):

    class Meta:
        model = RespuestaAQueja
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
        }
