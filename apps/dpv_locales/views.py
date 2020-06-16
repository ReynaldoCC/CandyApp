from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from django.db.models import Sum, Count, Case, When, F
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from .models import Local
from .forms import LocalForm
# from .tasks import list_local_revision
from apps.dpv_nomencladores.models import Municipio
from locales_viv import settings


# Create your views here.
@permission_required('dpv_locales.view_local', raise_exception=True)
def index(request):
    locales = Local.objects.none()
    try:
        perfil = request.user.perfil_usuario
        try:
            ct = perfil.centro_trabajo
            if ct.oc:
                locales = Local.objects.all()
            else:
                locales = Local.objects.filter(municipio=ct.municipio)
        except:
            print("no tiene centro de trabajo asociado")
    except:
        print("no tiene perfil asociado")
    return render(request, 'dpv_locales/list.html', {'locales': locales})


@permission_required('dpv_locales.add_local', raise_exception=True)
def local_add(request):
    if request.method == "POST":
        form = LocalForm(request.POST)
        if form.is_valid():
            local = form.save()
            local.perform_log(request=request, af=0)
            return redirect(to=reverse_lazy('locales_edit', kwargs={'id_local': local.id}))
        else:
            return render(request, 'dpv_locales/form.html', {'form': form})
    else:
        if not request.user.perfil_usuario.centro_trabajo.oc:
            local = Local()
            local.municipio = request.user.perfil_usuario.centro_trabajo.municipio
            form = LocalForm(instance=local)
        else:
            form = LocalForm()
        return render(request, 'dpv_locales/form.html', {'form': form})


# @permission_required('dpv_locales.view_local', raise_exception=True)
def stats(request, id_municipio=None, id_cpopular=None):
    result = []

    if not id_municipio and request.user.perfil_usuario.centro_trabajo.oc:
        if Local.objects.all().order_by('numero').count() > 0:
            for m in Municipio.objects.all():
                q = Local.objects.filter(municipio=m).aggregate(cant_viv=Sum('no_viviendas'),
                                                                cant_pend_viv=Sum('pendiente'),
                                                                cant_loc=Count('id'),
                                                                statales=Count(Case(When(estatal=True, then=1))),
                                                                propios=Count(Case(When(estatal=False, then=1))),
                                                                cant_viv_asoc=Count('vivienda_local__id'),
                                                                personas=Sum('vivienda_local__cantidad_persona'),
                                                                mujeres=Sum('vivienda_local__cantidad_mujeres'),
                                                                menores=Sum('vivienda_local__cantidad_menores'),
                                                                aclifim=Sum('vivienda_local__cantidad_aclifim'),
                                                                ancianos=Sum('vivienda_local__cantidad_anciano'))
                qm = {"nombre": m.nombre, "id": m.id, "tipo": 'municipio'}
                qr = dict(qm, **q)
                result.append(qr)
    elif not id_municipio and not request.user.perfil_usuario.centro_trabajo.oc:
        if Local.objects.filter(municipio=request.user.perfil_usuario.centro_trabajo.municipio).count() > 0:
            for cp in request.user.perfil_usuario.centro_trabajo.municipio.consejos.all().order_by('numero'):
                q = Local.objects.filter(consejo_popular=cp).aggregate(cant_viv=Sum('no_viviendas'),
                                                                       cant_pend_viv=Sum('pendiente'),
                                                                       cant_loc=Count('id'),
                                                                       statales=Count(Case(When(estatal=True, then=1))),
                                                                       propios=Count(Case(When(estatal=False, then=1))),
                                                                       cant_viv_asoc=Count('vivienda_local__id'),
                                                                       personas=Sum('vivienda_local__cantidad_persona'),
                                                                       mujeres=Sum('vivienda_local__cantidad_mujeres'),
                                                                       menores=Sum('vivienda_local__cantidad_menores'),
                                                                       aclifim=Sum('vivienda_local__cantidad_aclifim'),
                                                                       ancianos=Sum('vivienda_local__cantidad_anciano'))
                qm = {"nombre": cp.nombre, "id": cp.id, "tipo": 'consejo', "municipio": request.user.perfil_usuario.centro_trabajo.municipio.id}
                qr = dict(q, **qm)
                result.append(qr)
    elif id_cpopular:
        result = Local.objects.filter(consejo_popular_id=id_cpopular).annotate(cant_viv=F('no_viviendas'),
                                                                               cant_pend_viv=F('pendiente'),
                                                                               statales=F('estatal'),
                                                                               cant_viv_asoc=Count('vivienda_local__id'),
                                                                               cant_hab=Sum('vivienda_local__cantidad_persona'),
                                                                               mujeres=Sum('vivienda_local__cantidad_mujeres'),
                                                                               menores=Sum('vivienda_local__cantidad_menores'),
                                                                               aclifim=Sum('vivienda_local__cantidad_aclifim'),
                                                                               ancianos=Sum('vivienda_local__cantidad_anciano'))
    else:
        if Local.objects.filter(municipio=id_municipio).count() > 0:
            for cp in Municipio.objects.filter(id=id_municipio).first().consejos.all().order_by('numero'):
                q = Local.objects.filter(consejo_popular=cp).aggregate(cant_viv=Sum('no_viviendas'),
                                                                       cant_pend_viv=Sum('pendiente'),
                                                                       cant_loc=Count('id'),
                                                                       statales=Count(Case(When(estatal=True, then=1))),
                                                                       propios=Count(Case(When(estatal=False, then=1))),
                                                                       cant_viv_asoc=Count('vivienda_local__id'),
                                                                       personas=Sum('vivienda_local__cantidad_persona'),
                                                                       mujeres=Sum('vivienda_local__cantidad_mujeres'),
                                                                       menores=Sum('vivienda_local__cantidad_menores'),
                                                                       aclifim=Sum('vivienda_local__cantidad_aclifim'),
                                                                       ancianos=Sum('vivienda_local__cantidad_anciano'))
                qm = {"nombre": cp.nombre, "id": cp.id, "tipo": 'consejo', "municipio": id_municipio}
                qr = dict(q, **qm)
                result.append(qr)
    # return JsonResponse(data=result, safe=False)
    # print(result)
    return render(request, 'dpv_locales/estdistico.html', {'result': result})


@permission_required('dpv_locales.change_local', raise_exception=True)
def local_edit(request, id_local):
    lol = Local.objects.filter(id=id_local).first()
    form = LocalForm(instance=lol)
    if request.method == 'POST':
        form = LocalForm(request.POST, instance=lol)
        if form.is_valid():
            local = form.save()
            local.perform_log(request=request, af=1)
            return redirect(reverse_lazy('locales_list'))
    return render(request, 'dpv_locales/form.html', {'form': form, 'local': lol})


@permission_required('dpv_locales.view_local', raise_exception=True)
def local_detail(request, id_local):
    lol = get_object_or_404(Local, id=id_local)
    return render(request, 'dpv_locales/detail.html', {'local': lol})


@permission_required('dpv_locales.view_local', raise_exception=True)
def local_detail_full(request, id_local):
    lol = get_object_or_404(Local, id=id_local)
    return render(request, 'dpv_locales/detail_page.html', {'local': lol})


@permission_required('dpv_locales.delete_local', raise_exception=True)
def local_remove(request, id_local):
    lol = get_object_or_404(Local, id=id_local)
    if request.method == 'POST':
        if lol.vivienda_local.count() < 1:
            lol.perform_log(request=request, af=2)
            lol.delete()
            return redirect(reverse_lazy('locales_list'))
    return render(request, 'dpv_locales/delete.html', {'local': lol})


def local_revision(request, id_local=None):
    if not id_local:
        if settings.UPDATING_LOCALS == 0:
            settings.UPDATING_LOCALS = 1
            if request.user.perfil_usuario.centro_trabajo.oc:
                # list_local_revision.delay(list(Local.objects.all()))
                for local in Local.objects.all():
                    local.get_ok_data()
            else:
                # list_local_revision.delay(Local.objects.filter(municipio=request.user.perfil_usuario.centro_trabajo.municipio))
                for local in Local.objects.filter(municipio=request.user.perfil_usuario.centro_trabajo.municipio):
                    local.get_ok_data()
            settings.UPDATING_LOCALS = 0
            messages.info(request, _("Ya se comenzó a revisar el estado de los locales. Recivirá una notificación en el momento que se termine la tarea"))
            return redirect(reverse_lazy('locales_list'))
    else:
        Local.objects.filter(id=id_local).first().get_ok_data()
        return redirect(reverse_lazy('locales_list'))


def local_systeminfo(request, id_local):
    local = get_object_or_404(Local, id=id_local)
    return render(request, 'dpv_locales/system_data.html', {'local': local})


def local_verify(request):
    if request.method == 'GET':
        id, direccion_calle, direccion_numero, municipio = False, False, False, False
        if request.GET.get('direccion_calle'):
            direccion_calle = request.GET.get('direccion_calle')
        if request.GET.get('direccion_numero'):
            direccion_numero = request.GET.get('direccion_numero')
        if request.GET.get('municipio'):
            municipio = request.GET.get('municipio')
        id = request.GET.get('id')

        if direccion_calle and direccion_numero and municipio:
            if not Local.objects.filter(direccion_calle=direccion_calle,
                                        direccion_numero=direccion_numero,
                                        municipio=municipio).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("true", safe=False, status=200)
    return JsonResponse({"error": "method not Allowed"}, status=405)
