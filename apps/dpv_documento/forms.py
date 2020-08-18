from django import forms
from apps.dpv_nomencladores.models import Procedencia
from .models import DPVDocumento, TipoDPVDocumento
from django.utils.translation import gettext as _


class DPVDocumentoForm(forms.ModelForm):

    class Meta:
        model = DPVDocumento
        fields = ["no_refer",
                  "asunto",
                  "procedencia",
                  "destino",
                  "clasificacion",
                  "promovente",
                  "municipio",
                  "dir_cpopular",
                  "dir_calle",
                  "dir_numero",
                  "dir_entrecalle1",
                  "dir_entrecalle2",
                  "respuesta_a",
                  "archivo_digital", ]
        widgets = {
            "no_refer": forms.TextInput(attrs={"class": "form-control"}),
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
            "procedencia": forms.Select(attrs={"class": "form-control"}),
            "destino": forms.Select(attrs={"class": "form-control"}),
            "clasificacion": forms.Select(attrs={"class": "form-control"}),
            "promovente": forms.Select(attrs={"class": "form-control"}),
            "municipio": forms.Select(attrs={"class": "form-control"}),
            "dir_cpopular": forms.Select(attrs={"class": "form-control"}),
            "dir_calle": forms.Select(attrs={"class": "form-control"}),
            "dir_numero": forms.TextInput(attrs={"class": "form-control"}),
            "dir_entrecalle1": forms.Select(attrs={"class": "form-control"}),
            "dir_entrecalle2": forms.Select(attrs={"class": "form-control"}),
            "respuesta_a": forms.Select(attrs={"class": "form-control"}),
            "archivo_digital": forms.FileInput(attrs={"class": "form-control", "accept": "image/*,application/pdf"}),
        }


class DVPDocumentoEditForm(forms.ModelForm):

    class Meta:
        model = DPVDocumento
        fields = ["asunto", "destino", "respuesta_a", ]
        widgets = {
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
            "destino": forms.Select(attrs={"class": "form-control"}),
            "respuesta_a": forms.Select(attrs={"class": "form-control"}),
        }


class DVPDocumentoFechaEntregaForm(forms.ModelForm):

    class Meta:
        model = DPVDocumento
        fields = ["fecha_entrega", ]


class TipoDPVDocumentoForm(forms.ModelForm):

    class Meta:
        model = TipoDPVDocumento
        fields = ["nombre", "dias_proceso", "con_respuesta"]


    widgets = {
        "nombre": forms.TextInput(attrs={"class": "form-control"}),
    }


class DocsProcedenciaForm(forms.ModelForm):

    class Meta:
        model = Procedencia
        fields = '__all__'
