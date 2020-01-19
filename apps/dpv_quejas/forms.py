from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
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


class DamnificadoNaturalForm(forms.ModelForm):

    class Meta:
        model = DamnificadoNatural
        fields = (
                  'persona_natural',
        )
        widgets = {
            'persona_natural': forms.Select(attrs={"placeholder": "Seleccione una persona.", "class": "form-control"}),
        }


