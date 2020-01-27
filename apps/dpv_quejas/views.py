from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import F, Q, When, Case, BooleanField
from apps.dpv_respuesta.views import AprobadaRespuestaDtorView, AprobadaRespuestaJefeView
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
    aqform = AQPersonaNaturalForm()
    pnform = QPersonaNaturalForm()
    pjform = QPersonaJuridicaForm()
    tform = QTelefonoForm()
    eform = QEmailForm()
    orgform = QOrganismoForm()
    oform = QOrganizationForm()
    peform = QPrensaEscritaForm()
    gform = QGobiernoForm()
    if request.method == "POST":
        form = QuejaForm(request.POST)
        aqform = AQPersonaNaturalForm(request.POST)
        pnform = QPersonaNaturalForm(request.POST)
        pjform = QPersonaJuridicaForm(request.POST)
        tform = QTelefonoForm(request.POST)
        eform = QEmailForm(request.POST)
        orgform = QOrganismoForm(request.POST)
        oform = QOrganizationForm(request.POST)
        peform = QPrensaEscritaForm(request.POST)
        gform = QGobiernoForm(request.POST)

        if form.is_valid() and pnform.is_valid() and pjform.is_valid() and tform.is_valid() and eform.is_valid()\
                and orgform.is_valid() and oform.is_valid() and peform.is_valid() and aqform.is_valid()\
                and gform.is_valid():
            queja = form.save()
            person = pnform.save(commit=False)
            ent = pjform.save(commit=False)
            orgz = oform.save(commit=False)
            org = orgform.save(commit=False)
            tel = tform.save(commit=False)
            email = eform.save(commit=False)
            gob = gform.save(commit=False)

    return render(request, 'dpv_quejas/form.html', {'form': form,
                                                    'pnform': pnform,
                                                    'pjform': pjform,
                                                    'tform': tform,
                                                    'eform': eform,
                                                    'orgform': orgform,
                                                    'oform': oform,
                                                    'peform': peform,
                                                    'gform': gform,
                                                    'aqform': aqform})


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
