from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import PersonaNatural, PersonaJuridica


class PersonaNaturalForm(forms.ModelForm):

    class Meta:
        model = PersonaNatural
        fields = ('nombre',
                  'apellidos',
                  'ci',
                  'email_address',
                  'telefono',
                  'movil',
                  'genero',
                  'municipio',
                  'cpopular',
                  'direccion_calle',
                  'direccion_numero',
                  'direccion_entrecalle1',
                  'direccion_entrecalle2', )
        widgets = {
            'direccion_calle': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
            'direccion_entrecalle1': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
            'direccion_entrecalle2': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control"}),
            'municipio': forms.Select(attrs={"placeholder": "Seleccione un Municipio.", "class": "form-control"}),
            'cpopular': forms.Select(attrs={"placeholder": "Seleccione un Consejo Popular.", "class": "form-control"}),
            'genero': forms.Select(attrs={"placeholder": "Seleccione un Género.", "class": "form-control"}),
            'direccion_numero': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'ci': forms.TextInput(attrs={"placeholder": "CI", "class": "form-control"}),
            'nombre': forms.TextInput(attrs={"placeholder": "Nombre", "class": "form-control"}),
            'apellidos': forms.TextInput(attrs={"placeholder": "Apellidos", "class": "form-control"}),
            'email_address': forms.EmailInput(attrs={"placeholder": "Correo Electrónico", "class": "form-control"}),
            'telefono': forms.TextInput(attrs={"placeholder": "Teléfono Fijo", "class": "form-control"}),
            'movil': forms.TextInput(attrs={"placeholder": "Teléfono Movil", "class": "form-control"}),
        }

    def clean(self):
        if self.cleaned_data.get('movil') and self.cleaned_data.get('telefono'):
            if self.cleaned_data.get('movil') == self.cleaned_data.get('telefono'):
                raise ValidationError({'movil': 'Los Teléfonos no pueden ser iguales.'}, code='same_phone')
        if self.cleaned_data.get('direccion_calle') == self.cleaned_data.get('direccion_entrecalle1'):
            raise ValidationError({'direccion_entrecalle1':
                                   _('La primera entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('direccion_entrecalle2') == self.cleaned_data.get('direccion_calle'):
            raise ValidationError({'direccion_entrecalle2':
                                  _('La segunda entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('direccion_entrecalle1') == self.cleaned_data.get('direccion_entrecalle2'):
            raise ValidationError({'direccion_entrecalle2': _('Ambas entre calles no pueden ser iguales.')})
        return super(forms.ModelForm, self).clean()


class PersonaNaturalMForm(forms.ModelForm):

    class Meta:
        model = PersonaNatural
        fields = ('ci',
                  'telefono',
                  'movil',
                  'municipio',
                  'cpopular',
                  'direccion_calle',
                  'direccion_numero',
                  'direccion_entrecalle1',
                  'direccion_entrecalle2',
                  'genero', )
        widgets = {
            'direccion_calle': forms.Select(attrs={"placeholder": "Seleccione una Calle.",
                                                   "class": "form-control"}),
            'direccion_entrecalle1': forms.Select(attrs={"placeholder": "Seleccione una Calle.",
                                                         "class": "form-control"}),
            'direccion_entrecalle2': forms.Select(attrs={"placeholder": "Seleccione una Calle.",
                                                         "class": "form-control"}),
            'municipio': forms.Select(attrs={"placeholder": "Seleccione un Municipio.",
                                             "class": "form-control"}),
            'genero': forms.Select(attrs={"placeholder": "Seleccione un Género.", "class": "form-control"}),
            'direccion_numero': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'ci': forms.TextInput(attrs={"placeholder": "CI", "class": "form-control"}),
            'cpopular': forms.Select(attrs={"placeholder": "Seleccione un Consejo Popular.", "class": "form-control"}),
            'telefono': forms.TextInput(attrs={"placeholder": "Teléfono Fijo", "class": "form-control"}),
            'movil': forms.TextInput(attrs={"placeholder": "Teléfono Movil", "class": "form-control"}),
        }

    def clean(self):
        if self.cleaned_data.get('movil') and self.cleaned_data.get('telefono'):
            if self.cleaned_data.get('movil') == self.cleaned_data.get('telefono'):
                raise ValidationError({'movil': 'Los Teléfonos no pueden ser iguales.'}, code='same_phone')
        if self.cleaned_data.get('direccion_calle') == self.cleaned_data.get('direccion_entrecalle1'):
            raise ValidationError({'direccion_entrecalle1':
                                  _('La primera entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('direccion_entrecalle2') == self.cleaned_data.get('direccion_calle'):
            raise ValidationError({'direccion_entrecalle2':
                                  _('La segunda entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('direccion_entrecalle1') == self.cleaned_data.get('direccion_entrecalle2'):
            raise ValidationError({'direccion_entrecalle2': _('Ambas entre calles no pueden ser iguales.')})
        return super(forms.ModelForm, self).clean()


class PersonaJuridicaForm(forms.ModelForm):

    class Meta:
        model = PersonaJuridica
        fields = ('nombre',
                  'sigla',
                  'telefono',
                  'movil',
                  'nombre_contacto',
                  'email_address',
                  'direccion_calle',
                  'direccion_numero',
                  'direccion_entrecalle1',
                  'direccion_entrecalle2',
                  'municipio',
                  'cpopular',
                  'codigo_nit',
                  'codigo_reuup', )
        widgets = {
            'direccion_calle': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control select2"}),
            'direccion_entrecalle1': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control select2"}),
            'direccion_entrecalle2': forms.Select(attrs={"placeholder": "Seleccione una Calle.", "class": "form-control select2"}),
            'municipio': forms.Select(attrs={"placeholder": "Seleccione un Municipio.", "class": "form-control select2"}),
            'direccion_numero': forms.TextInput(attrs={"placeholder": "Número", "class": "form-control"}),
            'codigo_nit': forms.TextInput(attrs={"placeholder": "Código NiT", "class": "form-control"}),
            'nombre': forms.TextInput(attrs={"placeholder": "Nombre", "class": "form-control"}),
            'sigla': forms.TextInput(attrs={"placeholder": "Nombre", "class": "form-control"}),
            'nombre_contacto': forms.TextInput(attrs={"placeholder": "Nombre", "class": "form-control"}),
            'codigo_reuup': forms.TextInput(attrs={"placeholder": "Código Reeup", "class": "form-control"}),
            'email_address': forms.EmailInput(attrs={"placeholder": "Correo Electrónico", "class": "form-control"}),
            'telefono': forms.TextInput(attrs={"placeholder": "Teléfono Fijo", "class": "form-control"}),
            'movil': forms.TextInput(attrs={"placeholder": "Teléfono Movil", "class": "form-control"}),
            'cpopular': forms.Select(attrs={"placeholder": "Seleccione un Consejo Popular.", "class": "form-control select2"}),
        }

    def clean(self):
        if self.cleaned_data.get('movil') and self.cleaned_data.get('telefono'):
            if self.cleaned_data.get('movil') == self.cleaned_data.get('telefono'):
                raise ValidationError({'movil':'Los Teléfonos no pueden ser iguales.'}, code='same_phone')
        if self.cleaned_data.get('direccion_calle') == self.cleaned_data.get('direccion_entrecalle1'):
            raise ValidationError({'direccion_entrecalle1': _('La primera entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('direccion_entrecalle2') == self.cleaned_data.get('direccion_calle'):
            raise ValidationError({'direccion_entrecalle2': _('La segunda entre calle no puede ser igual a la calle de la dirección.')})
        if self.cleaned_data.get('direccion_entrecalle1') == self.cleaned_data.get('direccion_entrecalle2'):
            raise ValidationError({'direccion_entrecalle2': _('Ambas entre calles no pueden ser iguales.')})
        return super(forms.ModelForm, self).clean()


class PersonaNaturalProfileForm(forms.ModelForm):

    class Meta:
        model = PersonaNatural
        fields = ('telefono', 'email_address', )

        widgets = {
            'telefono': forms.TextInput(attrs={"placeholder": "Teléfono Fijo", "class": "form-control"}),
            'email_address': forms.EmailInput(attrs={"placeholder": "Correo Electrónico", "class": "form-control"}),
        }
