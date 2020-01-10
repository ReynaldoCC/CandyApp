import datetime

from django import forms
from .models import *


class ComplaintForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Complaint
        exclude = ('enter_date', 'is_natural', 'person_juridic', 'person_natural', 'status',
                   'anonymous', 'expiration_time', "department")


class AssignDepartmentForm(forms.Form):
    department = forms.ModelChoiceField(queryset=AreaTrabajo.objects.all(), label='Seleccione área de trabajo')


class TechnicianForm(forms.Form):
    technical = forms.ModelChoiceField(queryset=Technical.objects.all(), label='Disponibles')


class AssignedToTechnicalForm(forms.ModelForm):
    class Meta:
        model = AssignedToTechnician
        exclude = ('enter_date', 'complaint', 'assigned_by')


class FinishedComplaintForm(forms.ModelForm):
    class Meta:
        model = FinishedComplaint
        exclude = ('enter_date', 'technical', 'complaint',)


class AcceptedForm(forms.ModelForm):
    class Meta:
        model = Accepted
        exclude = ('finished_date', 'complaint', 'boss_accepted', 'technical_work_in_complaint', 'technical_args')
        labels = {'final_args': 'Argumentos Finales', 'answer': 'Respuesta'}


stat_history = {
    ('', 'Seleccione Estado'),
    ('Pendiente', 'Pendiente'),
    ('Esperando Asignación', 'Esperando Asignación'),
    ('Esperando Respuesta de Técnico', 'Esperando Respuesta de Técnico'),
    ('Esperando aceptación del jefe', 'Esperando aceptación del jefe'),
    ('Finalizada', 'Finalizada'),
}


class FilterForm(forms.Form):
    initial_time = forms.DateField(widget=forms.SelectDateWidget(), required=False)
    final_time = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now(), required=False)
    municipality = forms.ModelChoiceField(queryset=Municipio.objects.all(), required=False)
    days = forms.IntegerField(required=False)
    status = forms.ChoiceField(choices=stat_history, required=False, initial='')

    def clean(self):
        cleaned_data = super(FilterForm, self).clean()
        initial_time = cleaned_data.get('initial_time')
        final_time = cleaned_data.get('final_time')

        if final_time > datetime.date.today():
            raise forms.ValidationError("La fecha final debe ser antes del día de hoy")

        if initial_time and initial_time > final_time:
            raise forms.ValidationError("La fecha inicial debe ser antes de la fecha final")

        return cleaned_data
