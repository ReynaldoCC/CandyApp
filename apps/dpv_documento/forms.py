from django import forms
from .models import DPVDocumento, TipoDPVDocumento


class DPVDocumentoForm(forms.ModelForm):

    class Meta:
        model = DPVDocumento
        fields = ["no_refer",
                  "procedencia",
                  "promovente",
                  "clasificacion",
                  "asunto",
                  "destino",
                  "dir_calle",
                  "dir_numero",
                  "dir_entrecalle1",
                  "dir_entrecalle2",
                  "dir_cpopular",
                  "respuesta_a",
                  "municipio",
                  "archivo_digital", ]
        widgets = {
            "no_refer": forms.TextInput(attrs={"class": "form-control"}),
            "procedencia": forms.Select(attrs={"class": "form-control"}),
            "promovente": forms.Select(attrs={"class": "form-control"}),
            "clasificacion": forms.Select(attrs={"class": "form-control"}),
            "asunto": forms.TextInput(attrs={"class": "form-control"}),
            "destino": forms.Select(attrs={"class": "form-control"}),
            "dir_calle": forms.Select(attrs={"class": "form-control"}),
            "dir_numero": forms.TextInput(attrs={"class": "form-control"}),
            "dir_entrecalle1": forms.Select(attrs={"class": "form-control"}),
            "dir_entrecalle2": forms.Select(attrs={"class": "form-control"}),
            "dir_cpopular": forms.Select(attrs={"class": "form-control"}),
            "respuesta_a": forms.Select(attrs={"class": "form-control"}),
            "municipio": forms.Select(attrs={"class": "form-control"}),
            "archivo_digital": forms.FileInput(attrs={"class": "form-control"}),
        }


class TipoDPVDocumentoForm(forms.ModelForm):

    class Meta:
        model = TipoDPVDocumento
        fields = ["nombre", ]
