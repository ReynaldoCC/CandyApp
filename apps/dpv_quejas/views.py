from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import F, Q, When, Case, BooleanField
from apps.dpv_respuesta.views import AprobadaRespuestaDtorView, AprobadaRespuestaJefeView
from apps.dpv_persona.forms import PersonaNaturalForm
from .forms import *
from .models import *


@permission_required('dpv_quejass.view_queja', raise_exception=True)
def index(request):
    quejas = Queja.objects.all().annotate(radicada=Case(When(id__gt=0, then=True),
                                                        default=False,
                                                        output_field=BooleanField()),
                                          asignada_depto=Case(When(quejadpto__rechazada__isnull=True, then=True),
                                                              default=False,
                                                              output_field=BooleanField()),
                                          asignada_tecnico=Case(When(quejatecnico__rechazada__isnull=True, then=True),
                                                                default=False,
                                                                output_field=BooleanField()),
                                          respondida=Case(When(respuesta__rechazada__isnull=True, then=True),
                                                          default=False,
                                                          output_field=BooleanField()),
                                          aprobada_depto=Case(When(respuesta__apruebajefe__isnull=False, then=True),
                                                              default=False,
                                                              output_field=BooleanField()),
                                          aprobada_dir=Case(When(respuesta__apruebadtr__isnull=False, then=True),
                                                            default=False,
                                                            output_field=BooleanField()),
                                          )
    return render(request, 'dpv_quejas/list.html', {'quejas': quejas})


def agregar_queja(request):
    form = QuejaForm()
    pform = PersonaNaturalForm()
    dform = DamnificadoNaturalForm()
    if request.method == "POST":
        form = QuejaForm(request.POST)
        pform = PersonaNaturalForm(request.POST)
        dform = DamnificadoNaturalForm(request.POST)
        if form.is_valid() and pform.is_valid() and dform.is_valid():
            queja = form.save()
            damn = dform.save(commit=False)
            person = pform.save()

    return render(request, 'dpv_quejas/form.html', {'form': form, 'pform': pform, 'dform': dform})


def editar_queja(request, id_queja):
    return render(request, 'dpv_quejas/form.html')


def eliminar_queja(request, id_queja):
    return render(request, 'dpv_quejas/delete.html')


def asignar_queja_depto(request, id_queja):
    return render(request, 'dpv_quejas/asigna_depto.html')


def asignar_queja_tecnico(request, id_queja):
    return render(request, 'dpv_quejas/asigna_tecnico.html')


def responder_queja(request, id_queja):
    return render(request, 'dpv_quejas/responder.html')


def aprobar_respuesta_tecnico(request, id_queja):
    return render(request, 'dpv_quejas/jefe_aprueba.html')


def aprobar_respuesta_depto(request, id_queja):
    return render(request, 'dpv_quejas/director_aprueba.html')


def notificar_respuesta_queja(request, id_queja):
    return render(request, 'dpv_quejas/notificacion.html')


def rechazar_queja(request, id_queja):
    return render(request, 'dpv_quejas/rechazada.html')


def redirigir_queja(request, id_queja):
    return render(request, 'dpv_quejas/redirigida.html')


class AprobadaRespuestaQuejaDtorView(AprobadaRespuestaDtorView):
    success_url = reverse_lazy('quejas_list')

    def get_context_data(self, **kwargs):
        context = super(AprobadaRespuestaQuejaDtorView, self).get_context_data(**kwargs)
        print(**kwargs)
        # context['']

        return context


class AprobadaRespuestaQuejaJefeView(AprobadaRespuestaJefeView):
    success_url = reverse_lazy('quejas_list')
