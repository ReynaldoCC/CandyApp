from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Vivienda
from .forms import ViviendaForm
from django.contrib.auth.decorators import permission_required, login_required
from apps.dpv_locales.models import Local


# Create your views here.
@permission_required('dpv_viviendas.view_vivienda', raise_exception=True)
def index(request):
    viviendas = Vivienda.objects.none()
    try:
        perfil = request.user.perfil_usuario
        try:
            ct = perfil.centro_trabajo
            if ct.oc:
                viviendas = Vivienda.objects.all()
            else:
                viviendas = Vivienda.objects.filter(local_dado__municipio=ct.municipio)
        except:
            print("no tiene centro de trabajo asociado")
    except:
        print("no tiene perfil asociado")
    return render(request, "dpv_viviendas/list.html", {'viviendas': viviendas})


@permission_required('dpv_viviendas.add_vivienda', raise_exception=True)
def vivienda_add(request):
    if request.method == 'POST':
        form = ViviendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('vivienda_list'))
        else:
            return render(request, 'dpv_viviendas/form.html', {'form': form})
    else:
        form = ViviendaForm()
        return render(request, 'dpv_viviendas/form.html', {'form': form})


@permission_required('dpv_viviendas.change_vivienda', raise_exception=True)
def vivienda_edit(request, id_vivienda):
    viv = Vivienda.objects.filter(id=id_vivienda).first()
    if request.method == 'POST':
        form = ViviendaForm(request.POST, instance=viv)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('vivienda_list'))
    else:
        form = ViviendaForm(instance=viv)
    return render(request, 'dpv_viviendas/form.html', {'form': form})


@permission_required('dpv_viviendas.view_vivienda', raise_exception=True)
def vivienda_detail(request, id_vivienda):
    viv = Vivienda()
    try:
        perfil = request.user.perfil_usuario
        viv = Vivienda.objects.filter(id=id_vivienda).first()
        if not perfil.centro_trabajo.oc:
            if perfil.centro_trabajo.municipio != viv.local_dado.municpio:
                viv = Vivienda()
    except:
        print("El susuario no tiene perfil asociado")
    return  render(request, 'dpv_viviendas/detail.html', {'vivienda': viv})


@permission_required('dpv_viviendas.delete_vivienda', raise_exception=True)
def vivienda_delete(request, id_vivienda):
    viv = Vivienda()
    try:
        perfil = request.user.perfil_usuario
        viv = Vivienda.objects.filter(id=id_vivienda).first()
        if not perfil.centro_trabajo.oc:
            if perfil.centro_trabajo.municipio != viv.local_dado.municpio:
                if request.method == 'POST':
                    viv.delete()
                    return redirect(reverse_lazy('vivienda_list'))
                viv = Vivienda()
        else:
            if request.method == 'POST':
                viv.delete()
                return redirect(reverse_lazy('vivienda_list'))
    except:
        print("El susuario no tiene perfil asociado")
    return render(request, 'dpv_viviendas/delete.html', {'vivienda': viv})


@permission_required('dpv_viviendas.add_vivienda', raise_exception=True)
def vivienda_add_modal(request, id_local):
    viv = Vivienda()
    viv.local_dado = Local.objects.filter(id=id_local).first()
    form = ViviendaForm(instance=viv)
    if request.method == 'POST':
        form = ViviendaForm(request.POST, instance=viv)
        if form.is_valid():
            viv = form.save()
            return redirect(reverse_lazy('locales_edit', kwargs={'id_local': viv.local_dado.id}))
        else:
            return redirect(reverse_lazy('locales_list'))
    else:

        return render(request, 'dpv_viviendas/formodal.html', {'form': form, 'local': id_local})
