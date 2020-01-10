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
            'texto': forms.Textarea(attrs={"placeholder": "Nombre", "class": "form-control"}),
            'clasificacion': forms.Select(attrs={"placeholder": "Seleccione un Estado.", "class": "form-control select2"}),
        }


class ApruebaJefeForm(forms.ModelForm):

    class Meta:
        model = ApruebaJefe
        fields = (
                  'observacion_jefe',
                  'respuesta'

                  )
        widgets = {
            'observacion_jefe': forms.Textarea(attrs={"placeholder": "Nombre", "class": "form-control"}),
        }


class ApruebaDtrForm(forms.ModelForm):
    class Meta:
        model = ApruebaDtr
        fields = (
            'observacion_dtr',


        )
        widgets = {
            'observacion_jefe': forms.Textarea(attrs={"placeholder": "Nombre", "class": "form-control"}),
        }