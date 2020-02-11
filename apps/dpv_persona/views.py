from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.db.models import Count, F, Value, functions
from django.core import serializers
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
            model = form.save()
            model.perform_log(request=request, af=0)
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
            model = form.save()
            model.perform_log(request=request, af=0)
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
            model = form.save()
            model.perform_log(request=request, af=1)
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
            model = form.save()
            model.perform_log(request=request, af=1)
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
        persojur.perform_log(request=request, af=2)
        persojur.delete()
        return redirect(reverse_lazy('persona_juridica'))
    return render(request, 'dpv_persona/delete_persojur.html', {'persojur': persojur})


@permission_required('dpv_persona.delete_personanatural', raise_exception=True)
def delete_personat(request, id_personat):
    personat = PersonaNatural.objects.filter(id=id_personat).first()
    if request.method == 'POST':
        personat.perform_log(request=request, af=2)
        personat.delete()
        return redirect(reverse_lazy('persona_natural'))
    return render(request, 'dpv_persona/delete_personat.html', {'personat': personat})


def autofill_ci_personat(request):
    if request.method == 'POST':
        data = dict()
        ci = request.POST.get('ci')
        print(ci)
        cis = list()
        if ci:
            if len(ci) >= 3:
                personas = list([model_to_dict(mot) for mot in PersonaNatural.objects.filter(ci__icontains=ci)[:10]])
                data = personas
        else:
            data['personas'] = cis
        return JsonResponse(data=data, safe=False, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def found_person_by_ci(request):
    if request.method == 'POST':
        data = dict()
        ci = request.POST.get('ci')
        print(ci)
        if ci:
            person = PersonaNatural.objects.filter(ci=ci).first()
            if person:
                data['exist'] = True
                data['person'] = model_to_dict(person, exclude=['id', 'deleted_at'])
            else:
                data['exist'] = False
        return JsonResponse(data=data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def autofill_data_persojur(request):
    if request.method == 'POST':
        data = dict()
        nit = request.POST.get('codigo_nit')
        reuup = request.POST.get('codigo_reuup')
        nombre = request.POST.get('nombre')
        sigla = request.POST.get('sigla')
        nombre_contacto = request.POST.get('nombre_contacto')
        email_address = request.POST.get('email_address')
        telefono = request.POST.get('telefono')
        if nit:
            entities = list([model_to_dict(mot) for mot in PersonaJuridica.objects.filter(codigo_nit__icontains=nit)[:10]])
            data = entities
        elif reuup:
            entities = list([model_to_dict(mot) for mot in PersonaJuridica.objects.filter(codigo_reuup__icontains=reuup)[:10]])
            data = entities
        elif nombre:
            entities = list([model_to_dict(mot) for mot in PersonaJuridica.objects.filter(nombre__icontains=nombre)[:10]])
            data = entities
        elif sigla:
            entities = list([model_to_dict(mot) for mot in PersonaJuridica.objects.filter(sigla__icontains=sigla)[:10]])
            data = entities
        elif nombre_contacto:
            entities = list([model_to_dict(mot) for mot in PersonaJuridica.objects.filter(nombre_contacto__icontains=nombre_contacto)[:10]])
            data = entities
        elif email_address:
            entities = list([model_to_dict(mot) for mot in PersonaJuridica.objects.filter(email_address__icontains=email_address)[:10]])
            data = entities
        elif telefono:
            entities = list([model_to_dict(mot) for mot in PersonaJuridica.objects.filter(telefono__icontains=telefono)[:10]])
            data = entities
        return JsonResponse(data=data, safe=False, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def found_persojur_by_data(request):
    if request.method == 'POST':
        data = dict()
        nit = request.POST.get('codigo_nit')
        reuup = request.POST.get('codigo_reuup')
        nombre = request.POST.get('nombre')
        sigla = request.POST.get('sigla')
        nombre_contacto = request.POST.get('nombre_contacto')
        email_address = request.POST.get('email_address')
        telefono = request.POST.get('telefono')
        if nit:
            model = PersonaJuridica.objects.filter(codigo_nit=nit).first()
        elif reuup:
            model = PersonaJuridica.objects.filter(codigo_reuup=reuup).first()
        elif nombre:
            model = PersonaJuridica.objects.filter(nombre=nombre).first()
        elif sigla:
            model = PersonaJuridica.objects.filter(sigla=sigla).first()
        elif nombre_contacto:
            model = PersonaJuridica.objects.filter(nombre_contacto=nombre_contacto).first()
        elif email_address:
            model = PersonaJuridica.objects.filter(email_address=email_address).first()
        elif telefono:
            model = PersonaJuridica.objects.filter(telefono=telefono).first()
        else:
            model = None
        if model:
            data['exist'] = True
            data['empresa'] = model_to_dict(model, exclude=['id', 'deleted_at'])
        else:
            data['exist'] = False
        return JsonResponse(data=data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required()
def get_person_fields(request):
    personas = list(PersonaNatural.objects.all().annotate(
        text=functions.Concat(F('nombre'), Value(' '), F('apellidos'), Value(' ('), F('ci'), Value(')'))).values('id', 'nombre', 'apellidos', 'email_address', 'ci', 'text',))
    data = dict()
    data['personas'] = personas
    return JsonResponse(data=data, status=200)


@login_required()
def get_person_data(request, id_person):
    person =get_object_or_404(PersonaNatural, id=id_person)
    person_dic = model_to_dict(person, exclude=['deleted_at', ])
    person_dic['genero_nombre'] = person.genero.nombre
    person_dic['direccion_calle_nombre'] = person.direccion_calle.nombre
    person_dic['direccion_entrecalle1_nombre'] = person.direccion_entrecalle1.nombre
    person_dic['direccion_entrecalle2_nombre'] = person.direccion_entrecalle2.nombre
    person_dic['cpopular_nombre'] = person.cpopular.nombre
    person_dic['municipio_nombre'] = person.municipio.nombre
    return JsonResponse(data=person_dic, status=200)
