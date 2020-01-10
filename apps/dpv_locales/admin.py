from django.contrib import admin
from django.urls import path
from .models import Local
from apps.export_do.mixins import ExportDocsMixin


# Register your models here.
class LocalAdmin(admin.ModelAdmin, ExportDocsMixin):

    title_to_print = "CONTROL DE LOS LOCALES QUE SE HAN APROBADO EN LA COMISION DE DISTRIBUCIóN PROVINCIAL DEL CAP"

    fieldsets = [
         ('Dirección del local', {'fields': ['municipio', 'direccion_calle', 'direccion_numero', 'piso',
                                             'direccion_entre1', 'direccion_entre2', ]}),
         ('Datos del Local', {'fields': ['aprobado', 'estatal', 'no_viviendas', 'pendiente', 'organismo', 'acta',
                                         'acuerdo_DPV', 'acuerdoCAM', 'acuerdoPEM', 'acuerdoORG', ]}),
         ('Observaciones', {'fields': ['observaciones', ]}),
    ]

    list_display = ('municipio', 'direccion_calle', 'direccion_numero', 'piso', 'direccion_entre1',
                    'direccion_entre2', 'aprobado', 'pendiente', 'organismo', 'acta', 'fecha',
                    )
    list_filter = ('municipio__nombre', 'organismo__nombre', 'acta', 'fecha',
                   )
    search_fields = ('municipio__nombre', 'direccion_calle__nombre', 'direccion_numero', 'piso__nombre',
                     'direccion_entre1__nombre', 'direccion_entre2__nombre', 'organismo__nombre',
                     'fecha', )
    list_per_page = 25

    actions = ["export_as_csv", "export_as_xls", "export_as_pdf", ]

admin.site.site_header = "DPV La Habana"
admin.site.site_title = "Locales App"
admin.site.index_title = "Bienvenidos a la Aplicación de registro de Locales"
admin.site.register(Local, LocalAdmin)


