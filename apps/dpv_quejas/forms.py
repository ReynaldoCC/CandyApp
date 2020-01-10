from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import *


class QuejaForm(forms.ModelForm):

    class Meta:
        model = Queja
        fields = ('asunto',
                  'person_natural',
                  'empresa',
                  'dir_calle',
                  'dir_num',
                  'dir_entrecalle1',
                  'dir_entrecalle2',
                  'procedencia',
                  'referencia',
                  'estado',
                  'texto',
                  'clasificacion',
                  'respuesta',)
        widgets = {
            'dir_numero': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'dir_calle': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control select2"}),
            'dir_entrecalle1': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control select2"}),
            'dir_entrecalle2': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control select2"}),
            'person_natural': forms.Select(attrs={"placeholder": "Seleccione un Ciudadano.", "class": "form-control select2"}),
            'procedencia': forms.Select(attrs={"placeholder": "Seleccione una Procedencia.", "class": "form-control select2"}),
            'referencia': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'texto': forms.Textarea(attrs={"placeholder": "Nombre", "class": "form-control"}),
            'empresa': forms.Select(attrs={"placeholder": "Seleccione una Empresa.", "class": "form-control select2"}),
            'estado': forms.Select(attrs={"placeholder": "Seleccione un Estado.", "class": "form-control select2"}),
            'clasificacion': forms.Select(attrs={"placeholder": "Seleccione un Estado.", "class": "form-control select2"}),
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
        model = Queja
        fields = (
                  'dpto',
                  )
        widgets = {
            'dpto': forms.Select(attrs={"placeholder": "Seleccione un Departamento.", "class": "form-control select2"}),
        }


class AsignaQuejaTecnicoForm(forms.ModelForm):

    class Meta:
        model = Queja
        fields = (
                  'tecnico',
                  )
        widgets = {
            'tecnico': forms.Select(attrs={"placeholder": "Seleccione un Técnico.", "class": "form-control select2"}),
        }