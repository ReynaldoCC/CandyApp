from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Vivienda


class ViviendaForm(forms.ModelForm):

    class Meta:
        model = Vivienda
        fields = ('numero',
                  'destino',
                  'cantidad_persona',
                  'propietario',
                  'local_dado',
                  'concepto',
                  'fecha_propietario',
                  'aprobada',
                  'add_concepto', )
        widgets = {
            'numero': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'cantidad_persona': forms.TextInput(attrs={"placeholder": "Cantidad de Personas", "class": "form-control"}),
            'fecha_propietario': forms.TextInput(attrs={"placeholder": "Fecha de propiedad", "class": "form-control date"}),
            'add_concepto': forms.Textarea(attrs={"placeholder": "Sobre concepto", "class": "form-control"}),
            'propietario': forms.Select(attrs={"placeholder": "Seleccione un Propietario.", "class": "form-control select2"}),
            'concepto': forms.Select(attrs={"placeholder": "Seleccione un Concepto.", "class": "form-control select2"}),
            'destino': forms.Select(attrs={"placeholder": "Seleccione un Destino.", "class": "form-control select2"}),
            'local_dado': forms.Select(attrs={"placeholder": "Seleccione un Local.", "class": "form-control  select2"}),
            'aprobada': forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_fecha_propietario(self):
        if self.cleaned_data.get('fecha_propietario') >= timezone.datetime.today().date():
            raise ValidationError('La fecha de habitado de la vivienda no debe ser de hoy ni del futuro')
        return self.cleaned_data.get('fecha_propietario')