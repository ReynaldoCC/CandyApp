# -*- coding: utf-8 -*-
from django import forms
from .models import *

Month = [
    {
        1,
        "Enero",
    },
    {
        2,
        "Febrero",
    },
    {
        3,
        "Marzo",
    },
    {
        4,
        "Abril",
    },
    {
        5,
        "Mayo",
    },
    {
        6,
        "Junio",
    },
    {
        7,
        "Julio"
    },
    {
        8,
        "Agosto"
    },
    {
        9,
        "Septiembre"
    },
    {
        10,
        "Octubre"
    },
    {
        11,
        "Noviembre"
    },
    {
        12,
        "Diciembre"
    },
]


class TipoEventoForm(forms.Form):
    type_tipoevento = forms.CharField(label="Tipo", required=True, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Tipo","maxlength":255}))
    frecuencia_tipoevento = forms.ModelChoiceField(label="Frecuencia", required=False, queryset=Frecuencia.objects.all(), empty_label="",widget=forms.Select(attrs={"class":"form-control","prompt":"", "title":"Campo Obligatorio"}))


class FrecuenciaForm(forms.Form):
    name_frecuencia = forms.CharField(label="Nombre", required=True, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre","maxlength":255}))
    days_frecuencia = forms.CharField(label="Días", required=True, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Días"}))


class EventoForm(forms.Form):
    type_evento = forms.ModelChoiceField(label="Evento", required=True, queryset=TipoEvento.objects.all(), empty_label="",widget=forms.Select(attrs={"class":"form-control","prompt":"", "title":"Campo Obligatorio"}))
    date_programed_evento = forms.DateField(label="Fecha Programada", required=True, widget=forms.TextInput(attrs={"class":"form-control", "size":16}))
    site_evento = forms.CharField(label="Lugar", required=True, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Lugar","maxlength":255}))
    month_evento = forms.ChoiceField(label="Mes", required=True,widget=forms.Select(attrs={"class":"form-control","prompt":"", "title":"Campo Obligatorio"}))
    is_extraordinario_evento = forms.BooleanField(label="Es Extraordinario", widget=forms.CheckboxInput(attrs={"class":"form-control icheck", "placeholder":"Es Extraordinario"}))
    asunto_tema_evento = forms.CharField(label="Asunto", required=True, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Asunto","maxlength":255}))
    responsable_tema_evento = forms.ModelChoiceField(label="Responsable", required=True, queryset=User.objects.all().exclude(is_staff=True), empty_label="",widget=forms.Select(attrs={"class":"form-control","prompt":"", "title":"Campo Obligatorio"}))
    asunto_tema_sugerido_evento = forms.CharField(label="Asunto", required=True, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Asunto","maxlength":255}))
    body_acta_evento = forms.CharField(label="Texto", required=True, widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Texto", "style": "height: 110px"}))
    asunto_acuerdo_evento = forms.CharField(label="Acuerdo", required=True, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Acuerdo","maxlength":255}))
    date_finish_acuerdo_evento = forms.DateField(label= "Fecha de Cumplimiento", required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder': "Fecha de Cumplimiento", 'data-date-start-date': '+0d'}))
    responsables_acuerdo_evento = forms.ModelChoiceField(label="Responsables", required=True, queryset=User.objects.all().exclude(is_staff=True), empty_label="", widget=forms.SelectMultiple(attrs={"class":"form-control select2","prompt":"", "title":"Campo Obligatorio"}))