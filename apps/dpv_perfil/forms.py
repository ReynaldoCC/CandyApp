from django import forms
from .models import Perfil


# Put your Forms Here
class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ('notificacion_email', 'documentacion_email', 'avatar', 'centro_trabajo', 'depto_trabajo', )


class PerfilMForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ('notificacion_email', 'documentacion_email', 'centro_trabajo', 'depto_trabajo', )

        widgets = {
            'notificacion_email': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'documentacion_email': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'centro_trabajo': forms.Select(attrs={"placeholder": "Seleccione una Unidad.", "class": "form-control select2"}),
            'depto_trabajo': forms.Select(attrs={"placeholder": "Seleccione un Departamento.", "class": "form-control select2"}),
        }


class PerfilPForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ('notificacion_email', 'documentacion_email', 'avatar', )

        widgets = {
            'notificacion_email': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'documentacion_email': forms.CheckboxInput(attrs={"class": "form-check-input"}),
            'avatar': forms.FileInput(attrs={"class": "form-control"})
        }


