from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
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

@permission_required('dpv_respuesta.view_tecnico', raise_exception=True)
def index_tecnico(request):
    tecnicos = Tecnico.objects.all()
    return render(request, 'dpv_respuesta/list_tecnico.html', {'tecnicos': tecnicos})


@permission_required('dpv_respuesta.add_tecnico')
def add_tecnico(request):
    if request.method == 'POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request)
        return redirect('nomenclador_tecnico')
    else:
        form = TecnicoForm()
    return render(request, 'dpv_respuesta/form_tecnico.html', {'form': form})


@permission_required('dpv_respuesta.change_tecnico')
def update_tecnico(request, id_tecnico):
    tecnico = Tecnico.objects.get(id=id_tecnico)
    if request.method == 'POST':
        form = TecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request)
        return redirect('nomenclador_tecnico')
    else:
        form = TecnicoForm(instance=tecnico)
    return render(request, 'dpv_respuesta/form_tecnico.html', {'form': form, 'tecnico': tecnico})


@permission_required('dpv_respuesta.delete_tecnico')
def delete_tecnico(request, id_tecnico):
    tecnico = Tecnico.objects.get(id=id_tecnico)
    if request.method == 'POST':
        tecnico.perform_log(request=request)
        tecnico.delete()
        return redirect('nomenclador_tecnico')
    return render(request, 'dpv_respuesta/delete_tecnico.html', {'tecnico': tecnico})