from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import *


class RespuestaForm(forms.ModelForm):

    class Meta:
        model = Respuesta
        fields = (
                  'texto',
                  'clasificacion',
                  )
        widgets = {
            'texto': forms.Textarea(attrs={"placeholder": "Cuerpo de la respuesta", "class": "form-control"}),
        }


class ApruebaJefeForm(forms.ModelForm):

    class Meta:
        model = ApruebaJefe
        fields = (
                  'observacion_jefe',
                  )
        widgets = {
            'observacion_jefe': forms.Textarea(attrs={"placeholder": "Observación", "class": "form-control"}),
        }


class ApruebaDtrForm(forms.ModelForm):

    class Meta:
        model = ApruebaDtr
        fields = (
            'observacion_dtr',
        )
        widgets = {
            'observacion_dtr': forms.Textarea(attrs={"placeholder": "Observación", "class": "form-control"}),
        }


class RespuestaRechazadaForm(forms.ModelForm):

    class Meta:
        model = RespuestaRechazada
        fields = (
            'argumento',
        )
        widgets = {
            'argumento': forms.Textarea(attrs={"placeholder": "Argumento", "class": "form-control"}),
        }

class TecnicoForm(forms.ModelForm):
    profile = forms.ModelChoiceField(queryset=User.objects.all(),
                                              label=_("Técnicos"),
                                              widget=forms.Select(attrs={"class": "form-control select2"}))
    class Meta:
        model = Tecnico
        fields = ('profile',)