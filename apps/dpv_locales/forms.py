from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import Local


class LocalForm(forms.ModelForm):

    class Meta:
        model = Local
        fields = ('direccion_calle',
                  'direccion_numero',
                  'direccion_entre1',
                  'direccion_entre2',
                  'piso',
                  'municipio',
                  'consejo_popular',
                  'no_viviendas',
                  'pendiente',
                  'organismo',
                  'acta',
                  'acuerdoCAM',
                  'acuerdoPEM',
                  'acuerdoORG',
                  'acuerdo_DPV',
                  'aprobado',
                  'estatal',
                  'observaciones', )
        widgets = {
            'direccion_calle': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control select2"}),
            'direccion_entre1': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control select2"}),
            'direccion_entre2': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control select2"}),
            'piso': forms.Select(attrs={"placeholder": "Seleccione un Piso.", "class": "form-control select2"}),
            'municipio': forms.Select(attrs={"placeholder": "Seleccione un Municipio.", "class": "form-control select2"}),
            'organismo': forms.Select(attrs={"placeholder": "Seleccione u Organismo.", "class": "form-control select2"}),
            'consejo_popular': forms.Select(attrs={"placeholder": "Seleccione un Consejo Popular.", "class": "form-control select2"}),
            'direccion_numero': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'acuerdoCAM': forms.TextInput(attrs={"placeholder": "Acuerdo CAM", "class": "form-control"}),
            'acuerdoPEM': forms.TextInput(attrs={"placeholder": "Acuerdo PEM", "class": "form-control"}),
            'acuerdoORG': forms.TextInput(attrs={"placeholder": "Acuerdo Organismo", "class": "form-control"}),
            'acuerdo_DPV': forms.TextInput(attrs={"placeholder": "Acuerdo DPV", "class": "form-control"}),
            'acta': forms.TextInput(attrs={"placeholder": "Acta", "class": "form-control"}),
            'no_viviendas': forms.TextInput(attrs={"placeholder": "Total Viviendas", "class": "form-control"}),
            'pendiente': forms.TextInput(attrs={"placeholder": "Viviendas no Aprobadas", "class": "form-control"}),
            'aprobado': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'estatal': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'observaciones': forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean(self):
        if self.cleaned_data.get('direccion_calle') == self.cleaned_data.get('direccion_entre1'):
            raise ValidationError({'direccion_entre1': _('La primera entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('direccion_entre2') == self.cleaned_data.get('direccion_calle'):
            raise ValidationError({'direccion_entre2': _('La segunda entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('direccion_entre1') == self.cleaned_data.get('direccion_entre2'):
            raise ValidationError({'direccion_entre2': _('Ambas entre calles no pueden ser iguales.')})
        if self.cleaned_data.get('no_viviendas') and self.cleaned_data.get('pendiente'):
            if self.cleaned_data.get('no_viviendas') < self.cleaned_data.get('pendiente'):
                raise ValidationError({'pendiente': 'El número de viviendas pendientes de aprovación no puede ser mayor que el número de viviendas del local'})
        return super(forms.ModelForm, self).clean()