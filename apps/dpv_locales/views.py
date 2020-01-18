from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import Http404
from django.db.models import Sum, Count, Case, When
from django.contrib.auth.decorators import permission_required
from .models import Local
from .forms import LocalForm
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
def stats(request, id_municipio=None):
    result = []

    if not id_municipio and request.user.perfil_usuario.centro_trabajo.oc:
        if Local.objects.all().count() > 0:
            for m in Municipio.objects.all():
                q = Local.objects.filter(municipio=m).aggregate(cant_viv=Sum('no_viviendas'), cant_pend_viv=Sum('pendiente'), cant_loc=Count('id'), statales=Count(Case(When(estatal=True, then=1))), propios=Count(Case(When(estatal=False, then=1))))
                qm = {"nombre": m.nombre, "id": m.id, "tipo": 'municpio'}
                qr = dict(qm, **q)
                result.append(qr)
    elif not id_municipio and not request.user.perfil_usuario.centro_trabajo.oc:
        if Local.objects.filter(municipio=request.user.perfil_usuario.centro_trabajo.municipio).count() > 0:
            for cp in request.user.perfil_usuario.centro_trabajo.municipio.consejos.all():
                q = Local.objects.filter(consejo_popular=cp).aggregate(cant_viv=Sum('no_viviendas'), cant_pend_viv=Sum('pendiente'), cant_loc=Count('id'), statales=Count(Case(When(estatal=True, then=1))), propios=Count(Case(When(estatal=False, then=1))))
                qm = {"nombre": cp.nombre, "id": cp.id, "tipo": 'consejo'}
                qr = dict(q, **qm)
                result.append(qr)
    else:
        if Local.objects.filter(municipio=id_municipio).count() > 0:
            for cp in Municipio.objects.filter(id=id_municipio).first().consejos.all():
                q = Local.objects.filter(consejo_popular=cp).aggregate(cant_viv=Sum('no_viviendas'), cant_pend_viv=Sum('pendiente'), cant_loc=Count('id'), statales=Count(Case(When(estatal=True, then=1))), propios=Count(Case(When(estatal=False, then=1))))
                qm = {"nombre": cp.nombre, "id": cp.id, "tipo": 'consejo'}
                qr = dict(q, **qm)
                result.append(qr)

    return render(request, 'dpv_locales/estdistico.html', {'result': result})


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


def local_detail(request, id_local):
    lol = Local.objects.filter(id=id_local).first()
    if lol:
        return render(request, 'dpv_locales/detail.html', {'local': lol})
    else:
        raise Http404()


def local_remove(request, id_local):
    lol = Local.objects.filter(id=id_local).first()
    if lol:
        if request.method == 'POST':
            if lol.vivienda_local.count() < 1:
                lol.perform_log(request=request, af=2)
                lol.delete()
                return redirect(reverse_lazy('locales_list'))
        return render(request, 'dpv_locales/delete.html', {'local': lol})
    else:
        raise Http404()


def local_revision(request, id_local=None):
    if not id_local:
        if settings.UPDATING_LOCALS == 0:
            settings.UPDATING_LOCALS = 1
            if request.user.perfil_usuario.centro_trabajo.oc:
                for local in Local.objects.all():
                    local.get_ok_data()
            else:
                for local in Local.objects.filter(municipio=request.user.perfil_usuario.centro_trabajo.municipio):
                    local.get_ok_data()
            settings.UPDATING_LOCALS = 0
            return redirect(reverse_lazy('locales_list'))
    else:
        Local.objects.filter(id=id_local).first().get_ok_data()
        return redirect(reverse_lazy('locales_list'))


def local_systeminfo(reques, id_local):
    local = Local.objects.filter(id=id_local).first()
    return render(reques, 'dpv_locales/system_data.html', {'local': local})