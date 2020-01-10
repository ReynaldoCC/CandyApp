# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import *
from .forms import *


@permission_required('dpv_events.view_tipoevento')
def TipoEventoView(request):
    return render(request,'dpv_events/tipoevento.html',{'models':TipoEvento.objects.all(),'form':TipoEventoForm()})


@permission_required('dpv_events.add_tipoevento')
def create_tipoevento(request):
    data = {}
    form = TipoEventoForm(request.POST or None)

    if form.is_valid():
        type = request.POST["type_tipoevento"]

        permission = Permission.objects.create(name="Puede visualizar %s" % (type),content_type=ContentType.objects.get_for_model(TipoEvento),codename="view_tipoevento_%s" % (type.lower().replace(" ", "_")))

        model = TipoEvento()
        model.type = type
        if request.POST.get("frecuencia_tipoevento"):
            model.frecuencia_id = request.POST["frecuencia_tipoevento"]
        model.permission_id = permission.id
        model.save()
    return JsonResponse(data)


@permission_required('dpv_events.change_tipoevento')
def update_tipoevento(request):
    data = {}
    form = TipoEventoForm(request.POST or None)

    if form.is_valid():
        model = TipoEvento.objects.get(pk=request.POST['id'])
        model.type = form.cleaned_data["type_tipoevento"]
        if request.POST.get("frecuencia_tipoevento"):
            model.frecuencia_id = form.cleaned_data["frecuencia_tipoevento"]
        model.save()

    return JsonResponse(data)


@permission_required('dpv_events.delete_tipoevento')
def delete_tipoevento(request, tipoevento_id):
    model = TipoEvento.objects.get(pk=tipoevento_id)
    permission = Permission.objects.get(pk=model.permission_id)
    model.delete()
    permission.delete()
    return redirect('dpv_events:tipoevento')


@permission_required('dpv_events.view_frecuencia')
def FrecuenciaView(request):
    return render(request,'dpv_events/frecuencia.html',{'models':Frecuencia.objects.all(),'form':FrecuenciaForm()})


@permission_required('dpv_events.add_frecuencia')
def create_frecuencia(request):
    data = {}
    form = FrecuenciaForm(request.POST or None)

    if form.is_valid():
        model = Frecuencia()
        model.name = form.cleaned_data["name_frecuencia"]
        model.days = form.cleaned_data["days_frecuencia"]
        model.save()
    return JsonResponse(data)


@permission_required('dpv_events.change_frecuencia')
def update_frecuencia(request):
    data = {}
    form = FrecuenciaForm(request.POST or None)

    if form.is_valid():
        model = Frecuencia.objects.get(pk=request.POST['id'])
        model.name = form.cleaned_data["name_frecuencia"]
        model.days = form.cleaned_data["days_frecuencia"]
        model.save()

    return JsonResponse(data)


@permission_required('dpv_events.delete_frecuencia')
def delete_frecuencia(request, frecuencia_id):
    model = Frecuencia.objects.get(pk=frecuencia_id)
    model.delete()
    return redirect('dpv_events:frecuencia')


@permission_required('dpv_events.view_evento')
def EventosView(request):
    models = []

    for event in Evento.objects.all():
        if request.user.has_perm(event.type.permission):
            models.append(event)

    return render(request,'dpv_events/eventos.html',{'models':models,'form':EventoForm()})


@permission_required('dpv_events.view_evento')
def EventoView(request, event_id):
    return render(request,'dpv_events/evento.html',{'model':get_object_or_404(Evento.objects.all(), pk=event_id),'form':EventoForm()})


@permission_required('dpv_events.add_evento')
def create_evento(request):
    data = {}

    model = Evento()
    model.user_id = request.user.id
    model.type_id = request.POST["type_evento"]
    model.date_programed = request.POST["date_programed_evento"]
    model.site = request.POST["site_evento"]
    model.month = request.POST["month_evento"]

    if request.POST.get("is_extraordinario_evento"):
        model.is_extraordinario = True
    else:
        for event in Evento.objects.filter(type_id=request.POST['type_evento'], month=int(request.POST['month_evento'])):

            if not event.is_extraordinario:
                model.is_extraordinario = True

    model.save()

    tema = TemaEvento()
    tema.asunto = "Chequeo de Acuerdos"
    tema.evento_id = model.id
    tema.responsable_id = request.user.id
    tema.save()

    i = 0
    while request.POST.getlist('temas[' + str(i) + '][asunto]'):
        tema = TemaEvento()
        tema.asunto = str(request.POST['temas[' + str(i) + '][asunto]'])
        tema.evento_id = model.id
        tema.responsable_id = request.POST['temas[' + str(i) + '][responsable_id]']
        tema.save()
        i += 1

    tema = TemaEvento()
    tema.asunto = "Asuntos Sugeridos"
    tema.evento_id = model.id
    tema.responsable_id = request.user.id
    tema.save()

    return JsonResponse(data)


@permission_required('dpv_events.change_evento')
def update_evento(request):
    data = {}

    model = Evento.objects.get(pk=request.POST['id'])
    model.type_id = request.POST["type_evento"]
    model.date_programed = request.POST["date_programed_evento"]
    model.site = request.POST["site_evento"]
    model.month = request.POST["month_evento"]

    if request.POST.get("is_extraordinario_evento"):
        model.is_extraordinario = True
    else:
        model.is_extraordinario = False
        for event in Evento.objects.filter(type_id=request.POST['type_evento'],month=int(request.POST['month_evento'])).exclude(pk=model.id):
            if not event.is_extraordinario:
                model.is_extraordinario = True
    model.save()

    model.temaevento_set.filter(es_sugerido=False).delete()

    i = 0
    themes = []
    while request.POST.getlist('temas[' + str(i) + '][asunto]'):
        tema = TemaEvento()
        tema.asunto = str(request.POST['temas[' + str(i) + '][asunto]'])
        tema.evento_id = model.id
        tema.responsable_id = request.POST['temas[' + str(i) + '][responsable_id]']
        tema.save()
        themes.append({"id":i+1,"asunto": tema.asunto, "responsable_id": tema.responsable_id, "responsable_name": tema.responsable.username})
        i += 1

    data['event'] = {
        "id": model.id,
        "type": {
            "id": model.type_id,
            "type": model.type.type,
        },
        "date_programed": model.date_programed,
        "get_date_programed": model.get_date_programed,
        "time_programed": model.get_time_programed,
        "site": model.site,
        "month": model.month,
        "get_month": model.get_month,
        "is_extraordinario": model.is_extraordinario,
        "get_is_extraordinario": model.get_is_extraordinario,
        "themes": themes
    }

    return JsonResponse(data)


@permission_required('dpv_events.change_evento')
def done_evento(request, evento_id):
    model = Evento.objects.get(pk=evento_id)
    model.is_done = True
    model.save()
    return redirect('dpv_events:eventos')


@permission_required('dpv_events.delete_evento')
def delete_evento(request, evento_id):
    model = Evento.objects.get(pk=evento_id)
    model.delete()
    return redirect('dpv_events:eventos')


def verify_evento(request):
    data = {
        "exist": False
    }

    events = Evento.objects.filter(type_id=request.POST['type_id'], month=int(request.POST['month']))

    if request.POST.get('event_id'):
        events = events.exclude(pk=request.POST['event_id'])

    for event in events:

        if not event.is_extraordinario:
            data["exist"] = True
            data["type"] = event.type.type

    return JsonResponse(data)


@permission_required('dpv_events.add_temaevento')
def create_temaevento(request):

    data = {}

    if not TemaEvento.objects.filter(evento_id=request.POST['event_id'], es_sugerido=True):
        data['isfirst'] = True

    model = TemaEvento()
    model.asunto = request.POST['asunto_tema_sugerido_evento']
    model.evento_id = request.POST['event_id']
    model.responsable_id = request.user.id
    model.es_sugerido = True
    model.save()

    data["id"] = model.id
    data["asunto"] = model.asunto
    data["responsable_name"] = model.responsable.username

    return JsonResponse(data)


def aprobar_temaevento(request):

    model = TemaEvento.objects.get(pk=request.POST['theme_id'])
    model.es_sugerido = False
    model.save()

    data = {}

    return JsonResponse(data)


@permission_required('dpv_events.add_acta')
def create_acta(request):
    data = {}

    model = Acta()
    model.event_id = request.POST['event_id']
    model.body = request.POST['body_acta_evento']
    model.date_created = timezone.now()
    model.save()

    data['id'] = model.id
    data['code'] = model.code
    data['body'] = model.body

    return JsonResponse(data)


@permission_required('dpv_events.add_acuerdo')
def create_acuerdo(request):
    data = {}

    if not Acuerdo.objects.filter(event_id=request.POST['event_id']):
        data['isfirst'] = True

    model = Acuerdo()
    model.event_id = request.POST['event_id']
    model.asunto = request.POST['asunto_acuerdo_evento']
    model.date_finish = request.POST['date_finish_acuerdo_evento']
    model.save()

    responsables = request.POST.getlist('responsables_acuerdo_evento')
    for responsable in responsables:
        ra = ResponsableAcuerdo()
        ra.responsable_id = responsable
        ra.acuerdo_id = model.id
        ra.save()

    data['id'] = model.id
    data['code'] = model.code
    data['asunto'] = model.asunto
    data['date_finish'] = model.date_finish
    data['responsables'] = request.user.username
    data['state'] = 'En Proceso'

    return JsonResponse(data)