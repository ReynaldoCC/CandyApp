# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Dpv_eventsConfig(AppConfig):
    name = "apps.dpv_events"
    verbose_name = _("Consejos y Reuniones")
    menu = "dpv_events/menu/main.html"
    active = True
    owned = True
    menuable = True
    parent = True      # Si el modulo es un submodulo de otro en el menu (y solo en el menu)
    child_of = ''
    model_data = ['Evento'] #.objects.all().count() # Cantidad de registros del elemento funcamental del modulo o app
    name_data = 'Eventos Registrados' # Nombre o texto a mostrar del sisginificado de dichos registros
    route_data = 'dpv_events:eventos' # ruta principal del modulo
