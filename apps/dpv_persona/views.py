from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from .forms import PersonaJuridicaForm, PersonaNaturalForm
from .models import PersonaNatural, PersonaJuridica


# Create your views here.
@login_required()
def index(request):
    cantpers = PersonaNatural.objects.all().count()
    cantents = PersonaJuridica.objects.all().count()
    return render(request, 'dpv_persona/list.html', {'cantpers': cantpers, 'cantents': cantents})


@permission_required('dpv_persona.view_personajuridica', raise_exception=True)
def index_persojur(request):
    persojurs = PersonaJuridica.objects.all()
    return render(request, 'dpv_persona/list_persojur.html', {'personajuridicas': persojurs})


@permission_required('dpv_persona.view_personanatural', raise_exception=True)
def index_personat(request):
    person = PersonaNatural.objects.all()
    return render(request, 'dpv_persona/list_personat.html', {'personas': person})


@permission_required('dpv_persona.add_personajuridica', raise_exception=True)
def add_personjur(request):
    if request.method == 'POST':
        form = PersonaJuridicaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('persona_juridica'))
        else:
            return render(request, 'dpv_persona/form_persojur.html', {'form': form})
    else:
        form = PersonaJuridicaForm()
        return render(request, 'dpv_persona/form_persojur.html', {'form': form})


@permission_required('dpv_persona.add_personajuridica', raise_exception=True)
def add_personat(request):
    if request.method == 'POST':
        form = PersonaNaturalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('persona_natural'))
        else:
            return render(request, 'dpv_persona/form_personat.html', {'form': form})
    else:
        form = PersonaNaturalForm()
        return render(request, 'dpv_persona/form_personat.html', {'form': form})


@permission_required('dpv_persona.change_personajuridica', raise_exception=True)
def edit_personat(request, id_personat):
    pers = PersonaNatural.objects.filter(id=id_personat).first()
    if request.method == 'POST':
        form = PersonaNaturalForm(request.POST, instance=pers)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('persona_natural'))
    else:
        form = PersonaNaturalForm(instance=pers)
    return render(request, 'dpv_persona/form_personat.html', {'form': form})


@permission_required('dpv_persona.change_personajuridica', raise_exception=True)
def edit_persojur(request, id_persojur):
    ents = PersonaJuridica.objects.filter(id=id_persojur).first()
    if request.method == 'POST':
        form = PersonaJuridicaForm(request.POST, instance=ents)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('persona_juridica'))
    else:
        form = PersonaJuridicaForm(instance=ents)
    return render(request, 'dpv_persona/form_persojur.html', {'form': form})


@permission_required('dpv_persona.view_personajuridica', raise_exception=True)
def detail_persojur(request, id_persojur):
    persojur = PersonaJuridica.objects.filter(id=id_persojur).first()
    return render(request, 'dpv_persona/detail_persojur.html', {'persojur': persojur})


@permission_required('dpv_persona.view_personanatural', raise_exception=True)
def detail_personat(request, id_personat):
    personat = PersonaNatural.objects.filter(id=id_personat).first()
    return render(request, 'dpv_persona/detail_personat.html', {'personat': personat})


@permission_required('dpv_persona.delete_personajuridica', raise_exception=True)
def delete_persojur(request, id_persojur):
    persojur = PersonaJuridica.objects.filter(id=id_persojur).first()
    if request.method == 'POST':
        persojur.delete()
        return redirect(reverse_lazy('persona_juridica'))
    return render(request, 'dpv_persona/delete_persojur.html', {'persojur': persojur})


@permission_required('dpv_persona.delete_personanatural', raise_exception=True)
def delete_personat(request, id_personat):
    personat = PersonaNatural.objects.filter(id=id_personat).first()
    if request.method == 'POST':
        personat.delete()
        return redirect(reverse_lazy('persona_natural'))
    return render(request, 'dpv_persona/delete_personat.html', {'personat': personat})