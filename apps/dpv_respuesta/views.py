from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from .models import *


class AprobadaRespuestaJefeView(CreateView):
    model = ApruebaJefe
    fields = ['observacion_jefe', ]
    form_class = ApruebaJefeForm
    template_name = 'dpv_respuesta/respuesta_aprobada_j.html'


class AprobadaRespuestaDtorView(CreateView):
    model = ApruebaDtr
    fields = ['observacion_dtr', ]
    form_class = ApruebaDtrForm
    template_name = 'dpv_respuesta/respuesta_aprobada_d.html'


class RechazarRespuestaView(CreateView):
    model = RespuestaRechazada
    fields = ['argumento', ]
    form_class = RespuestaRechazadaForm
    template_name = 'dpv_respuesta/respuesta_rechazada.html'

