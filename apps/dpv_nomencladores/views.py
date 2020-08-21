from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy

from apps.dpv_persona.forms import PersonaJuridicaForm, PersonaNaturalForm
from apps.dpv_persona.models import PersonaJuridica, PersonaNatural

from .forms import *
from .models import *


# Create your views here.
@login_required()
def index(request):
    muns = Municipio.objects.all().count()
    pros = Provincia.objects.all().count()
    cpps = ConsejoPopular.objects.all().count()
    cocp = Concepto.objects.all().count()
    dest = Destino.objects.all().count()
    orgs = Organismo.objects.all().count()
    gnes = Genero.objects.all().count()
    piso = Piso.objects.all().count()
    call = Calle.objects.all().count()
    cent = CentroTrabajo.objects.all().count()
    artr = AreaTrabajo.objects.all().count()
    ca = CodificadorAsunto.objects.all().count()
    tpqueja = TipoQueja.objects.all().count()
    proc = Procedencia.objects.all().count()
    tpproc = TipoProcedencia.objects.all().count()
    est = Estado.objects.all().count()
    clasresp = ClasificacionRespuesta.objects.all().count()
    return render(request, 'dpv_nomencladores/list.html', {'municipios': muns, 'provincias': pros, 'consejos': cpps, 'conceptos': cocp, 'destinos': dest, 'organismos': orgs, \
                                                           'generos': gnes, 'pisos': piso, 'calles': call, 'unidades': cent, 'deptos': artr, 'codifasunto': ca, 'tqueja':tpqueja, \
                                                           'procedencia': proc, 'tprocedencia':tpproc, 'estado': est, 'clasfrespuesta': clasresp})


# ----------------------------------------- Provincia -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_provincia', raise_exception=True)
def index_provincia(request):
    provincias = Provincia.objects.all()
    return render(request, 'dpv_nomencladores/list_provincia.html', {'provincias': provincias})


@permission_required('dpv_nomencladores.add_provincia')
def add_provincia(request):
    if request.method == 'POST':
        form = ProvinciaForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_provincia')
    else:
        form = ProvinciaForm()
    return render(request, 'dpv_nomencladores/form_provincia.html', {'form': form})


@permission_required('dpv_nomencladores.change_provincia')
def update_provincia(request, id_provincia):
    provincia = Provincia.objects.get(id=id_provincia)
    if request.method == 'POST':
        form = ProvinciaForm(request.POST, instance=provincia)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_provincia')
    else:
        form = ProvinciaForm(instance=provincia)
    return render(request, 'dpv_nomencladores/form_provincia.html', {'form': form, 'provincia': provincia})


@permission_required('dpv_nomencladores.delete_provincia')
def delete_provincia(request, id_provincia):
    provincia = Provincia.objects.get(id=id_provincia)
    if request.method == 'POST':
        provincia.perform_log(request=request, af=2)
        provincia.delete()
        return redirect('nomenclador_provincia')
    return render(request, 'dpv_nomencladores/delete_provincia.html', {'provincia': provincia})


@permission_required('dpv_nomencladores.view_provincia')
def verify_provincia(request):
    if request.method == 'GET':
        nombre = numero = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not Provincia.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if numero:
            if not Provincia.objects.filter(numero__iexact=numero).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# ----------------------------------------- Municipio ----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_municipio', raise_exception=True)
def index_municipio(request):
    municipios = Municipio.objects.all()
    return render(request, 'dpv_nomencladores/list_municipio.html', {'municipios': municipios})


@permission_required('dpv_nomencladores.add_municipio')
def add_municipio(request):
    if request.method == 'POST':
        form = MunicipioForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_municipio')
    else:
        form = MunicipioForm()
    return render(request, 'dpv_nomencladores/form_municipio.html', {'form': form})


@permission_required('dpv_nomencladores.change_municipio')
def update_municipio(request, id_municipio):
    municipio = Municipio.objects.get(id=id_municipio)
    if request.method == 'POST':
        form = MunicipioForm(request.POST, instance=municipio)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_municipio')
    else:
        form = MunicipioForm(instance=municipio)
    return render(request, 'dpv_nomencladores/form_municipio.html', {'form': form, 'municipio': municipio})


@permission_required('dpv_nomencladores.delete_municipio')
def delete_municipio(request, id_municipio):
    municipio = Municipio.objects.get(id=id_municipio)
    if request.method == 'POST':
        municipio.perform_log(request=request, af=2)
        municipio.delete()
        return redirect('nomenclador_municipio')
    return render(request, 'dpv_nomencladores/delete_municipio.html', {'municipio': municipio})


@permission_required('dpv_nomencladores.view_municipio')
def verify_municipio(request):
    if request.method == 'GET':
        nombre = numero = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not Municipio.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if numero:
            if not Municipio.objects.filter(numero__iexact=numero).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


@login_required()
def filter_municipio_prov(request, id_prov):
    province = get_object_or_404(Provincia, id=id_prov)
    municipios = list(Municipio.objects.filter(provincia=province).values('id', 'nombre'))
    return JsonResponse(data=municipios, safe=False, status=200)


# ------------------------------------ ConsejoPopular -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_consejopopular', raise_exception=True)
def index_consejopopular(request):
    if request.is_ajax():
        consejopopulars = list(model_to_dict(cpopular) for cpopular in ConsejoPopular.objects.all())
        return JsonResponse(data=consejopopulars, safe=False, status=200)
    else:
        consejopopulars = ConsejoPopular.objects.all()
        return render(request, 'dpv_nomencladores/list_consejopopular.html', {'consejopopulars': consejopopulars})


@login_required()
def filter_by_muncp(request, id_municipio):
    try:
        cpopulares = list(model_to_dict(cpop) for cpop in ConsejoPopular.objects.filter(municipio__id=id_municipio))
        return JsonResponse(data=cpopulares, safe=False, status=200)
    except:
        return JsonResponse({"error": "Invalid id value"})


@permission_required('dpv_nomencladores.add_consejopopular')
def add_consejopopular(request):
    if request.method == 'POST':
        form = ConsejoPopularForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_consejopopular')
    else:
        form = ConsejoPopularForm()
    return render(request, 'dpv_nomencladores/form_consejopopular.html', {'form': form})


@login_required()
def add_cpopular_json(request):
    data = {}
    status = 200
    if request.method == 'POST':
        form = ConsejoPopularForm(request.POST)
        if form.is_valid():
            nombre_cpop = form.cleaned_data.get('nombre')
            municipio = form.cleaned_data.get('municipio')
            numero = form.cleaned_data.get('numero')
            if int(numero) <= 0:
                ultimo_numero_str = ConsejoPopular.objects.order_by('id').last().numero
                ultimo_numero = int(ultimo_numero_str)
                numero = str(ultimo_numero + 1)
            cpop, created = ConsejoPopular.objects.get_or_create(nombre=nombre_cpop, defaults={"municipio": municipio,
                                                                                               "numero": numero})
            data = model_to_dict(cpop)
            if created:
                status = 201
            return JsonResponse(data=data, status=status)
        data['errors'] = form.errors
        status = 400
        return JsonResponse(data=data, status=status)
    return JsonResponse({"error": "method not allowed"}, status=405)


@permission_required('dpv_nomencladores.change_consejopopular')
def update_consejopopular(request, id_consejopopular):
    consejopopular = ConsejoPopular.objects.get(id=id_consejopopular)
    if request.method == 'POST':
        form = ConsejoPopularForm(request.POST, instance=consejopopular)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_consejopopular')
    else:
        form = ConsejoPopularForm(instance=consejopopular)
    return render(request, 'dpv_nomencladores/form_consejopopular.html', {'form': form,
                                                                          'consejopopular': consejopopular})


@permission_required('dpv_nomencladores.delete_consejopopular')
def delete_consejopopular(request, id_consejopopular):
    consejopopular = ConsejoPopular.objects.get(id=id_consejopopular)
    if request.method == 'POST':
        consejopopular.perform_log(request=request, af=2)
        consejopopular.delete()
        return redirect('nomenclador_consejopopular')
    return render(request, 'dpv_nomencladores/delete_consejopopular.html', {'consejopopular': consejopopular})


@permission_required('dpv_nomencladores.view_consejopopular')
def verify_consejopopular(request):
    if request.method == 'GET':
        nombre = numero = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not ConsejoPopular.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if numero:
            if not ConsejoPopular.objects.filter(numero__iexact=numero).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# ------------------------------------------- Calle -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_calle', raise_exception=True)
def index_calle(request):
    if request.is_ajax():
        calles = list(model_to_dict(calle) for calle in Calle.objects.all())
        return JsonResponse(data=calles, safe=False, status=200)
    else:
        calles = Calle.objects.all()
    return render(request, 'dpv_nomencladores/list_calle.html', {'calles': calles})


@permission_required('dpv_nomencladores.add_calle')
def add_calle(request):
    if request.method == 'POST':
        form = CalleForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_calle')
    else:
        form = CalleForm()
    return render(request, 'dpv_nomencladores/form_calle.html', {'form': form})


@permission_required('dpv_nomencladores.add_calle')
def add_calle_on_user(request):
    data = {}
    if request.method == 'POST':
        form = CalleForm(request.POST or None)
        # print(form.data)
        if form.is_valid():
            # print(form.cleaned_data)
            calle = form.save()
            # print(calle)
            data = {'nombre': calle.nombre,
                    'id': calle.id,
                    }
            calle.perform_log(request=request, af=0)
        else:
            data = {
                'errmsg': form.errors
            }
            return JsonResponse(data, status=400)
    return JsonResponse(data)


@login_required()
def add_calle_json(request):
    data = {}
    status = 200
    if request.method == 'POST':
        form = CalleForm(request.POST)
        if form.is_valid():
            nombre_calle = form.cleaned_data.get('nombre')
            municipios = form.cleaned_data.get('municipios')
            calle, created = Calle.objects.get_or_create(nombre=nombre_calle)
            if municipios and not municipios in calle.municipios.all():
                if calle.municipios.count() == 0:
                    calle.municipios.set(municipios)
                else:
                    calle.municipios.add(municipios)
            data = model_to_dict(calle)
            if created:
                status = 201
            return JsonResponse(data=data, status=status)
        data['errors'] = form.errors
        status = 400
        return JsonResponse(data=data, status=status)
    return JsonResponse({"error": "method not allowed"}, status=405)


@login_required()
def filter_by_municipio(request, id_municipio):
    try:
        calles = list(model_to_dict(calle, fields=["id", "nombre"]) for calle in Calle.objects.filter(municipios__id=id_municipio))
        return JsonResponse(data=calles, safe=False, status=200)
    except:
        return JsonResponse({"error": "Invalid id value"}, status=400)


@permission_required('dpv_nomencladores.add_calle')
def agree_calle(request, select_id):
    calleform = CalleForm()
    calle = Calle()
    return render(request, 'dpv_nomencladores/form_calle_async.html', {'form': calleform, 'calle': calle, 'value': select_id})


@permission_required('dpv_nomencladores.change_calle')
def update_calle(request, id_calle):
    calle = Calle.objects.get(id=id_calle)
    if request.method == 'POST':
        form = CalleForm(request.POST, instance=calle)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_calle')
    else:
        form = CalleForm(instance=calle)
    return render(request, 'dpv_nomencladores/form_calle.html', {'form': form, 'calle': calle})


@permission_required('dpv_nomencladores.delete_calle')
def delete_calle(request, id_calle):
    calle = Calle.objects.get(id=id_calle)
    if request.method == 'POST':
        calle.perform_log(request=request, af=2)
        calle.delete()
        return redirect('nomenclador_calle')
    return render(request, 'dpv_nomencladores/delete_calle.html', {'calle': calle})


@permission_required('dpv_nomencladores.view_calle')
def verify_calle(request):
    if request.method == 'GET':
        nombre = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not Calle.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# ------------------------------------------- Piso -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_piso', raise_exception=True)
def index_piso(request):
    pisos = Piso.objects.all()
    return render(request, 'dpv_nomencladores/list_piso.html', {'pisos': pisos})


@permission_required('dpv_nomencladores.add_piso')
def add_piso(request):
    if request.method == 'POST':
        form = PisoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_piso')
    else:
        form = PisoForm()
    return render(request, 'dpv_nomencladores/form_piso.html', {'form': form})


@permission_required('dpv_nomencladores.change_piso')
def update_piso(request, id_piso):
    piso = Piso.objects.get(id=id_piso)
    if request.method == 'POST':
        form = PisoForm(request.POST, instance=piso)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_piso')
    else:
        form = PisoForm(instance=piso)
    return render(request, 'dpv_nomencladores/form_piso.html', {'form': form, 'piso': piso})


@permission_required('dpv_nomencladores.delete_piso')
def delete_piso(request, id_piso):
    piso = Piso.objects.get(id=id_piso)
    if request.method == 'POST':
        piso.perform_log(request=request, af=2)
        piso.delete()
        return redirect('nomenclador_piso')
    return render(request, 'dpv_nomencladores/delete_piso.html', {'piso': piso})


@permission_required('dpv_nomencladores.view_piso')
def verify_piso(request):
    if request.method == 'GET':
        nombre = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not Piso.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# --------------------------------------- Organismo -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_organismo', raise_exception=True)
def index_organismo(request):
    organismos = Organismo.objects.all()
    return render(request, 'dpv_nomencladores/list_organismo.html', {'organismos': organismos})


@permission_required('dpv_nomencladores.add_organismo')
def add_organismo(request):
    if request.method == 'POST':
        form = OrganismoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_organismo')
    else:
        form = OrganismoForm()
    return render(request, 'dpv_nomencladores/form_organismo.html', {'form': form})


@permission_required('dpv_nomencladores.change_organismo')
def update_organismo(request, id_organismo):
    organismo = Organismo.objects.get(id=id_organismo)
    if request.method == 'POST':
        form = OrganismoForm(request.POST, instance=organismo)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_organismo')
    else:
        form = OrganismoForm(instance=organismo)
    return render(request, 'dpv_nomencladores/form_organismo.html', {'form': form, 'organismo': organismo})


@permission_required('dpv_nomencladores.delete_organismo')
def delete_organismo(request, id_organismo):
    organismo = Organismo.objects.get(id=id_organismo)
    if request.method == 'POST':
        organismo.perform_log(request=request, af=2)
        organismo.delete()
        return redirect('nomenclador_organismo')
    return render(request, 'dpv_nomencladores/delete_organismo.html', {'organismo': organismo})


def autofill_organismo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            if len(nombre) >= 3:
                organismos = [model_to_dict(mot) for mot in Organismo.objects.filter(nombre__icontains=nombre)[:10]]
        return JsonResponse(data=organismos, safe=False, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def found_organismo_by_name(request):
    if request.method == 'POST':
        data = dict()
        nombre = request.POST.get('nombre')
        print(nombre)
        if nombre:
            organismo = Organismo.objects.filter(nombre=nombre).first()
            if organismo:
                data['exist'] = True
                data['organismo'] = model_to_dict(organismo)
            else:
                data['exist'] = False
        return JsonResponse(data=data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ------------------------------------------- Destino -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_destino', raise_exception=True)
def index_destino(request):
    destinos = Destino.objects.all()
    return render(request, 'dpv_nomencladores/list_destino.html', {'destinos': destinos})


@permission_required('dpv_nomencladores.add_destino')
def add_destino(request):
    if request.method == 'POST':
        form = DestinoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_destino')
    else:
        form = DestinoForm()
    return render(request, 'dpv_nomencladores/form_destino.html', {'form': form})


@permission_required('dpv_nomencladores.change_destino')
def update_destino(request, id_destino):
    destino = Destino.objects.get(id=id_destino)
    if request.method == 'POST':
        form = DestinoForm(request.POST, instance=destino)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_destino')
    else:
        form = DestinoForm(instance=destino)
    return render(request, 'dpv_nomencladores/form_destino.html', {'form': form, 'destino': destino})


@permission_required('dpv_nomencladores.delete_destino')
def delete_destino(request, id_destino):
    destino = Destino.objects.get(id=id_destino)
    if request.method == 'POST':
        destino.perform_log(request=request, af=2)
        destino.delete()
        return redirect('nomenclador_destino')
    return render(request, 'dpv_nomencladores/delete_destino.html', {'destino': destino})


@permission_required('dpv_nomencladores.view_destino')
def verify_destino(request):
    if request.method == 'GET':
        nombre = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not Destino.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# ------------------------------------------- Concepto -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_concepto', raise_exception=True)
def index_concepto(request):
    conceptos = Concepto.objects.all()
    return render(request, 'dpv_nomencladores/list_concepto.html', {'conceptos': conceptos})


@permission_required('dpv_nomencladores.add_concepto')
def add_concepto(request):
    if request.method == 'POST':
        form = ConceptoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_concepto')
    else:
        form = ConceptoForm()
    return render(request, 'dpv_nomencladores/form_concepto.html', {'form': form})


@permission_required('dpv_nomencladores.change_concepto')
def update_concepto(request, id_concepto):
    concepto = Concepto.objects.get(id=id_concepto)
    if request.method == 'POST':
        form = ConceptoForm(request.POST, instance=concepto)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_concepto')
    else:
        form = ConceptoForm(instance=concepto)
    return render(request, 'dpv_nomencladores/form_concepto.html', {'form': form, 'concepto': concepto})


@permission_required('dpv_nomencladores.delete_concepto')
def delete_concepto(request, id_concepto):
    concepto = Concepto.objects.get(id=id_concepto)
    if request.method == 'POST':
        concepto.perform_log(request=request, af=2)
        concepto.delete()
        return redirect('nomenclador_concepto')
    return render(request, 'dpv_nomencladores/delete_concepto.html', {'concepto': concepto})


@permission_required('dpv_nomencladores.view_concepto')
def verify_concepto(request):
    if request.method == 'GET':
        nombre = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not Concepto.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# ------------------------------------------- Genero -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_genero', raise_exception=True)
def index_genero(request):
    generos = Genero.objects.all()
    return render(request, 'dpv_nomencladores/list_genero.html', {'generos': generos})


@permission_required('dpv_nomencladores.add_genero')
def add_genero(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_genero')
    else:
        form = GeneroForm()
    return render(request, 'dpv_nomencladores/form_genero.html', {'form': form})


@permission_required('dpv_nomencladores.change_genero')
def update_genero(request, id_genero):
    genero = Genero.objects.get(id=id_genero)
    if request.method == 'POST':
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_genero')
    else:
        form = GeneroForm(instance=genero)
    return render(request, 'dpv_nomencladores/form_genero.html', {'form': form, 'genero': genero})


@permission_required('dpv_nomencladores.delete_genero')
def delete_genero(request, id_genero):
    genero = Genero.objects.get(id=id_genero)
    if request.method == 'POST':
        genero.perform_log(request=request, af=2)
        genero.delete()
        return redirect('nomenclador_genero')
    return render(request, 'dpv_nomencladores/delete_genero.html', {'genero': genero})


@permission_required('dpv_nomencladores.view_genero')
def verify_genero(request):
    if request.method == 'GET':
        nombre = sigla = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('sigla'):
            sigla = request.GET.get('sigla')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not Genero.objects.filter(nsigla__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if sigla:
            if not Genero.objects.filter(sigla__iexact=sigla).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# ------------------------------------- AreaTrabajo -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_areatrabajo', raise_exception=True)
def index_areatrabajo(request):
    departamentos = AreaTrabajo.objects.all()
    return render(request, 'dpv_nomencladores/list_areatrabajo.html', {'departamentos': departamentos})


@permission_required('dpv_nomencladores.add_areatrabajo')
def add_areatrabajo(request):
    if request.method == 'POST':
        form = AreaTrabajoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_areatrab')
    else:
        form = AreaTrabajoForm()
    return render(request, 'dpv_nomencladores/form_areatrabajo.html', {'form': form})


@permission_required('dpv_nomencladores.change_areatrabajo')
def update_areatrabajo(request, id_areatrabajo):
    areatrabajo = AreaTrabajo.objects.get(id=id_areatrabajo)
    if request.method == 'POST':
        form = AreaTrabajoForm(request.POST, instance=areatrabajo)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_areatrab')
    else:
        form = AreaTrabajoForm(instance=areatrabajo)
    return render(request, 'dpv_nomencladores/form_areatrabajo.html', {'form': form, 'areatrabajo': areatrabajo})


@permission_required('dpv_nomencladores.delete_areatrabajo')
def delete_areatrabajo(request, id_areatrabajo):
    areatrabajo = AreaTrabajo.objects.get(id=id_areatrabajo)
    if request.method == 'POST':
        areatrabajo.perform_log(request=request, af=2)
        areatrabajo.delete()
        return redirect('nomenclador_areatrab')
    return render(request, 'dpv_nomencladores/delete_areatrabajo.html', {'areatrabajo': areatrabajo})


@permission_required('dpv_nomencladores.view_areatrabajo')
def verify_areatrabajo(request):
    if request.method == 'GET':
        nombre = numero = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not AreaTrabajo.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if numero:
            if not AreaTrabajo.objects.filter(numero__iexact=numero).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# ------------------------------------- CentroTrabajo -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_centrotrabajo', raise_exception=True)
def index_centrotrabajo(request):
    unidades = CentroTrabajo.objects.all()
    return render(request, 'dpv_nomencladores/list_centrotrabajo.html', {'unidades': unidades})


@permission_required('dpv_nomencladores.add_centrotrabajo')
def add_centrotrabajo(request):
    if request.method == 'POST':
        form = CentroTrabajoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_centrab')
    else:
        form = CentroTrabajoForm()

    return render(request, 'dpv_nomencladores/form_centrotrabajo.html', {'form': form})


@permission_required('dpv_nomencladores.change_centrotrabajo')
def update_centrotrabajo(request, id_centrotrabajo):
    centrotrabajo = CentroTrabajo.objects.get(id=id_centrotrabajo)
    if request.method == 'POST':
        form = CentroTrabajoForm(request.POST, instance=centrotrabajo)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_centrab')
    else:
        form = CentroTrabajoForm(instance=centrotrabajo)
    return render(request, 'dpv_nomencladores/form_centrotrabajo.html', {'form': form, 'centrotrabajo': centrotrabajo})


@permission_required('dpv_nomencladores.delete_centrotrabajo')
def delete_centrotrabajo(request, id_centrotrabajo):
    centrotrabajo = CentroTrabajo.objects.get(id=id_centrotrabajo)
    if request.method == 'POST':
        centrotrabajo.perform_log(request=request, af=2)
        centrotrabajo.delete()
        return redirect('nomenclador_centrab')
    return render(request, 'dpv_nomencladores/delete_centrotrabajo.html', {'centrotrabajo': centrotrabajo})


@permission_required('dpv_nomencladores.view_centrotrabajo')
def verify_centrotrabajo(request):
    if request.method == 'GET':
        nombre = numero = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not CentroTrabajo.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if numero:
            if not CentroTrabajo.objects.filter(numero__iexact=numero).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", safe=False, status=400)
    return JsonResponse("", safe=False, status=405)


# ------------------------------------------- CodificadorAsunto ----------------------------------------------------
@permission_required('dpv_nomencladores.view_codificadorasunto', raise_exception=True)
def index_codificadorasunto(request):
    codificadorasuntos = CodificadorAsunto.objects.all()
    return render(request, 'dpv_nomencladores/list_codificadorasunto.html', {'codificadorasuntos': codificadorasuntos})


@permission_required('dpv_nomencladores.add_codificadorasunto')
def add_codificadorasunto(request):
    if request.method == 'POST':
        form = CodificadorAsuntoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_codificadorasunto')
    else:
        form = CodificadorAsuntoForm()
    return render(request, 'dpv_nomencladores/form_codificadorasunto.html', {'form': form})


@permission_required('dpv_nomencladores.change_codificadorasunto')
def update_codificadorasunto(request, id_codificadorasunto):
    codificadorasunto = CodificadorAsunto.objects.get(id=id_codificadorasunto)
    if request.method == 'POST':
        form = CodificadorAsuntoForm(request.POST, instance=codificadorasunto)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_codificadorasunto')
    else:
        form = CodificadorAsuntoForm(instance=codificadorasunto)
    return render(request, 'dpv_nomencladores/form_codificadorasunto.html', {'form': form,
                                                                             'codificadorasunto': codificadorasunto})


@permission_required('dpv_nomencladores.delete_codificadorasunto')
def delete_codificadorasunto(request, id_codificadorasunto):
    codificadorasunto = CodificadorAsunto.objects.get(id=id_codificadorasunto)
    if request.method == 'POST':
        codificadorasunto.perform_log(request=request, af=2)
        codificadorasunto.delete()
        return redirect('nomenclador_codificadorasunto')
    return render(request, 'dpv_nomencladores/delete_codificadorasunto.html', {'codificadorasunto': codificadorasunto})


@permission_required('dpv_nomencladores.view_codificadorasunto')
def verify_codificadorasunto(request):
    if request.method == 'GET':
        nombre = numero = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not CodificadorAsunto.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if numero:
            if not CodificadorAsunto.objects.filter(numero__iexact=numero).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# ---------------------------------------- TipoQueja -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_tipoqueja', raise_exception=True)
def index_tipoqueja(request):
    tipoquejas = TipoQueja.objects.all()
    return render(request, 'dpv_nomencladores/list_tipoqueja.html', {'tipoquejas': tipoquejas})


@permission_required('dpv_nomencladores.add_tipoqueja')
def add_tipoqueja(request):
    if request.method == 'POST':
        form = TipoQuejaForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_tipoqueja')
    else:
        form = TipoQuejaForm()
    return render(request, 'dpv_nomencladores/form_tipoqueja.html', {'form': form})


@permission_required('dpv_nomencladores.change_tipoqueja')
def update_tipoqueja(request, id_tipoqueja):
    tipoqueja = TipoQueja.objects.get(id=id_tipoqueja)
    if request.method == 'POST':
        form = TipoQuejaForm(request.POST, instance=tipoqueja)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_tipoqueja')
    else:
        form = TipoQuejaForm(instance=tipoqueja)
    return render(request, 'dpv_nomencladores/form_tipoqueja.html', {'form': form, 'tipoqueja': tipoqueja})


@permission_required('dpv_nomencladores.delete_tipoqueja')
def delete_tipoqueja(request, id_tipoqueja):
    tipoqueja = TipoQueja.objects.get(id=id_tipoqueja)
    if request.method == 'POST':
        tipoqueja.perform_log(request=request, af=2)
        tipoqueja.delete()
        return redirect('nomenclador_tipoqueja')
    return render(request, 'dpv_nomencladores/delete_tipoqueja.html', {'tipoqueja': tipoqueja})


@permission_required('dpv_nomencladores.view_tipoqueja')
def verify_tipoqueja(request):
    if request.method == 'GET':
        nombre = numero = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not TipoQueja.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if numero:
            if not TipoQueja.objects.filter(numero__iexact=numero).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# -------------------------------------- Procedencia -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_procedencia', raise_exception=True)
def index_procedencia(request):
    procedencias = Procedencia.objects.all()
    return render(request, 'dpv_nomencladores/list_procedencia.html', {'procedencias': procedencias})





@permission_required('dpv_nomencladores.add_procedencia')
def add_procedencia(request):
    form = ProcedenciaForm(prefix='procedencia')
    peform = PrensaEscritaForm(prefix='pe', empty_permitted=True, use_required_attribute=False)
    aqform = PersonaNaturalForm(prefix='person_procedence', empty_permitted=True, use_required_attribute=False)
    tform = TelefonoForm(prefix='telefono', empty_permitted=True, use_required_attribute=False)
    eform = EmailForm(prefix='email', empty_permitted=True, use_required_attribute=False)
    pjform = PersonaJuridicaForm(prefix='empresa', empty_permitted=True, use_required_attribute=False)
    oform = OrganizationForm(prefix='organiza', empty_permitted=True, use_required_attribute=False)
    orgform = OrganismoForm(prefix='organism', empty_permitted=True, use_required_attribute=False)
    pwform = ProcedenciaWebForm(prefix='web', empty_permitted=True, use_required_attribute=False)

    if request.method == 'POST':
        data = {}
        status = 200

        procedence_form = AnonimoForm()

        if request.POST.get('pe-nombre'):
            pe = PrensaEscrita.objects.filter(nombre=request.POST.get('pe-nombre'))
            if pe:
                procedence_form = peform = PrensaEscritaForm(request.POST, prefix='pe', use_required_attribute=False,
                                                              instance=pe.first(), empty_permitted=True)
            else:
                procedence_form = peform = PrensaEscritaForm(request.POST, prefix='pe',
                                                              use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('person_procedence-ci') and request.POST.get('person_procedence-nombre'):
            pn = PersonaNatural.objects.filter(ci=request.POST.get('person_procedence-ci'))
            if pn:
                procedence_form = aqform = PersonaNaturalForm(request.POST, prefix='person_procedence',
                                                                use_required_attribute=False,
                                                                instance=pn.first(), empty_permitted=True)
            else:
                procedence_form = aqform = PersonaNaturalForm(request.POST, prefix='person_procedence',
                                                                use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('web-perfil') and request.POST.get('web-email'):
            pw = ProcedenciaWeb.objects.filter(perfil__iexact=request.POST.get('web-perfil'),
                                               email=request.POST.get('web-email'),
                                               red_social=request.POST.get('web-red_social'))
            if pw:
                procedence_form = pwform = ProcedenciaWebForm(request.POST, prefix='web',
                                                              use_required_attribute=False,
                                                              instance=pw.first(), empty_permitted=True)
            else:
                procedence_form = pwform = ProcedenciaWebForm(request.POST, prefix='web',
                                                              use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('organism-nombre'):
            org = ProcedenciaWeb.objects.filter(nombre__iexact=request.POST.get('organism-nombre'))
            if org:
                procedence_form = orgform = OrganismoForm(request.POST, prefix='organism',
                                                          use_required_attribute=False,
                                                          instance=org.first(), empty_permitted=True)
            else:
                procedence_form = orgform = OrganismoForm(request.POST, prefix='organism',
                                                          use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('telefono-numero'):
            tel = Telefono.objects.filter(numero=request.POST.get('telefono-numero'))
            if tel:
                procedence_form = tform = TelefonoForm(request.POST, prefix='telefono', use_required_attribute=False,
                                                        instance=tel.first(), empty_permitted=True)
            else:
                procedence_form = tform = TelefonoForm(request.POST, prefix='telefono', use_required_attribute=False,
                                                        empty_permitted=True)
        elif request.POST.get('email-email'):
            ema = Email.objects.filter(email=request.POST.get('email-email'))
            if ema:
                procedence_form = EmailForm(request.POST, prefix='email', use_required_attribute=False,
                                                     instance=ema.first(), empty_permitted=True)
            else:
                procedence_form = EmailForm(request.POST, prefix='email', use_required_attribute=False,
                                                     empty_permitted=True)
        elif request.POST.get('empresa-nombre') and request.POST.get('empresa-codigo_nit') and request.POST.get('empresa-codigo_reuup'):
            pj = PersonaJuridica.objects.filter(codigo_nit=request.POST.get('empresa-codigo_nit'),
                                                codigo_reuup=request.POST.get('empresa-codigo_reuup'),
                                                nombre=request.POST.get('empresa-nombre'))
            if pj:
                procedence_form = pjform = PersonaJuridicaForm(request.POST, prefix='empresa',
                                                                instance=pj.first(), empty_permitted=True,
                                                                use_required_attribute=False)
            else:
                procedence_form = pjform = PersonaJuridicaForm(request.POST, prefix='empresa', empty_permitted=True,
                                                                use_required_attribute=False)
        elif request.POST.get('organiza-nombre'):
            org = Organizacion.objects.filter(nombre=request.POST.get('organiza-nombre')[0])
            if org:
                procedence_form = oform = OrganizationForm(request.POST, prefix='organiza',
                                                            use_required_attribute=False,
                                                            instance=org.first(), empty_permitted=True)
            else:
                procedence_form = oform = OrganizationForm(request.POST, prefix='organiza',
                                                            use_required_attribute=False,
                                                            empty_permitted=True)

        if procedence_form.is_valid():
            content_type_form = procedence_form.save()
            if content_type_form:
                content_type = ContentType.objects.get_for_model(content_type_form)
                proc = Procedencia.objects.create(objecto_contenido=content_type_form, tipo_contenido=content_type, id_objecto=content_type_form.id)
                proc.save_and_log(request=request, af=0)
            else:
                proc, pcreated = Procedencia.objects.get_or_create(nombre="Anónimo", tipo=TipoProcedencia.objects.filter(id=1).first())
            if request.is_ajax():
                data = model_to_dict(proc)
                data["message"] = "procedencia agregada satisfactoriamente"
                return JsonResponse(data=data, status=status)
            else:
                messages.success(request, "procedencia agregada satisfactoriamente")
                return redirect(reverse_lazy("nomenclador_procedencia"))
        else:
            data['errors'] = form.errors
            status = 400
        return JsonResponse(data=data, status=status)

    return render(
        request,
        'dpv_nomencladores/form_procedencia.html',
        {
            'form': form,
            'pjform': pjform,
            'tform': tform,
            'eform': eform,
            'oform': oform,
            'orgform': orgform,
            'pwform': pwform,
            'peform': peform,
            'aqform': aqform
        }
    )


@permission_required('dpv_nomencladores.change_procedencia')
def update_procedencia(request, id_procedencia):
    procedencia = Procedencia.objects.get(id=id_procedencia)
    if request.method == 'POST':
        form = ProcedenciaForm(request.POST, instance=procedencia)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_procedencia')
    else:
        form = ProcedenciaForm(instance=procedencia)
    return render(request, 'dpv_nomencladores/form_procedencia.html', {'form': form, 'procedencia': procedencia})


@permission_required('dpv_nomencladores.delete_procedencia')
def delete_procedencia(request, id_procedencia):
    procedencia = Procedencia.objects.get(id=id_procedencia)
    if request.method == 'POST':
        procedencia.perform_log(request=request, af=2)
        messages.warning(request=request, message=_("No se puede eliminar procedencias de esta lista verifique con el administrador del sistema para ver que desea hacer y si es posible"))
        # procedencia.delete()
        return redirect('nomenclador_procedencia')
    return render(request, 'dpv_nomencladores/delete_procedencia.html', {'procedencia': procedencia})


# ------------------------------------------- TipoProcedencia ----------------------------------------------------------
@permission_required('dpv_nomencladores.view_tipoprocedencia', raise_exception=True)
def index_tipoprocedencia(request):
    tipoprocedencias = TipoProcedencia.objects.all()
    return render(request, 'dpv_nomencladores/list_tipoprocedencia.html', {'tipoprocedencias': tipoprocedencias})


@permission_required('dpv_nomencladores.add_tipoprocedencia')
def add_tipoprocedencia(request):
    if request.method == 'POST':
        form = TipoProcedenciaForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_tipoprocedencia')
    else:
        form = TipoProcedenciaForm()
    return render(request, 'dpv_nomencladores/form_tipoprocedencia.html', {'form': form})


@permission_required('dpv_nomencladores.change_tipoprocedencia')
def update_tipoprocedencia(request, id_tipoprocedencia):
    tipoprocedencia = TipoProcedencia.objects.get(id=id_tipoprocedencia)
    if request.method == 'POST':
        form = TipoProcedenciaForm(request.POST, instance=tipoprocedencia)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_tipoprocedencia')
    else:
        form = TipoProcedenciaForm(instance=tipoprocedencia)
    return render(request, 'dpv_nomencladores/form_tipoprocedencia.html',{'form': form, 'tipoprocedencia': tipoprocedencia})


@permission_required('dpv_nomencladores.delete_tipoprocedencia')
def delete_tipoprocedencia(request, id_tipoprocedencia):
    tipoprocedencia = TipoProcedencia.objects.get(id=id_tipoprocedencia)
    if request.method == 'POST':
        tipoprocedencia.perform_log(request=request, af=0)
        tipoprocedencia.delete()
        return redirect('nomenclador_tipoprocedencia')
    return render(request, 'dpv_nomencladores/delete_tipoprocedencia.html', {'tipoprocedencia': tipoprocedencia})


@permission_required('dpv_nomencladores.view_tipoprocedencia')
def verify_tipoprocedencia(request):
    if request.method == 'GET':
        nombre = numero = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('numero'):
            numero = request.GET.get('numero')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not TipoProcedencia.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if numero:
            if not TipoProcedencia.objects.filter(numero__iexact=numero).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# ------------------------------------------- Estado -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_estado', raise_exception=True)
def index_estado(request):
    estados = Estado.objects.all()
    return render(request, 'dpv_nomencladores/list_estado.html', {'estados': estados})


@permission_required('dpv_nomencladores.add_estado')
def add_estado(request):
    if request.method == 'POST':
        form = EstadoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_estado')
    else:
        form = EstadoForm()
    return render(request, 'dpv_nomencladores/form_estado.html', {'form': form})


@permission_required('dpv_nomencladores.change_estado')
def update_estado(request, id_estado):
    estado = Estado.objects.get(id=id_estado)
    if request.method == 'POST':
        form = EstadoForm(request.POST, instance=estado)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_estado')
    else:
        form = EstadoForm(instance=estado)
    return render(request, 'dpv_nomencladores/form_estado.html', {'form': form, 'estado': estado})


@permission_required('dpv_nomencladores.delete_estado')
def delete_estado(request, id_estado):
    estado = Estado.objects.get(id=id_estado)
    if request.method == 'POST':
        estado.perform_log(request=request, af=2)
        estado.delete()
        return redirect('nomenclador_estado')
    return render(request, 'dpv_nomencladores/delete_estado.html', {'estado': estado})


@permission_required('dpv_nomencladores.view_estado')
def verify_estado(request):
    if request.method == 'GET':
        nombre = numero = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not Estado.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# --------------------------------------- ClasificacionRespuesta ------------------------------------------------
@permission_required('dpv_nomencladores.view_clasificacionrespuesta', raise_exception=True)
def index_clasificacionrespuesta(request):
    clasificacionrespuestas = ClasificacionRespuesta.objects.all()
    return render(request,
                  'dpv_nomencladores/list_clasificacionrespuesta.html',
                  {'clasificacionrespuestas': clasificacionrespuestas})


@permission_required('dpv_nomencladores.add_clasificacionrespuesta')
def add_clasificacionrespuesta(request):
    if request.method == 'POST':
        form = ClasificacionRespuestaForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_clasificacionrespuesta')
    else:
        form = ClasificacionRespuestaForm()
    return render(request, 'dpv_nomencladores/form_clasificacionrespuesta.html', {'form': form})


@permission_required('dpv_nomencladores.change_clasificacionrespuesta')
def update_clasificacionrespuesta(request, id_clasificacionrespuesta):
    clasificacionrespuesta = ClasificacionRespuesta.objects.get(id=id_clasificacionrespuesta)
    if request.method == 'POST':
        form = ClasificacionRespuestaForm(request.POST, instance=clasificacionrespuesta)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_clasificacionrespuesta')
    else:
        form = ClasificacionRespuestaForm(instance=clasificacionrespuesta)
    return render(request, 'dpv_nomencladores/form_clasificacionrespuesta.html',
                  {'form': form, 'clasificacionrespuesta': clasificacionrespuesta})


@permission_required('dpv_nomencladores.delete_clasificacionrespuesta')
def delete_clasificacionrespuesta(request, id_clasificacionrespuesta):
    clasificacionrespuesta = ClasificacionRespuesta.objects.get(id=id_clasificacionrespuesta)
    if request.method == 'POST':
        clasificacionrespuesta.perform_log(request=request, af=2)
        clasificacionrespuesta.delete()
        return redirect('nomenclador_clasificacionrespuesta')
    return render(request,
                  'dpv_nomencladores/delete_clasificacionrespuesta.html',
                  {'clasificacionrespuesta': clasificacionrespuesta})


@permission_required('dpv_nomencladores.view_clasificacionrespuesta')
def verify_clasificacionrespuesta(request):
    if request.method == 'GET':
        nombre = codigo = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('codigo'):
            codigo = request.GET.get('codigo')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not ClasificacionRespuesta.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if codigo:
            if not ClasificacionRespuesta.objects.filter(codigo__iexact=codigo).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# --------------------------------------- PrensaEscrita ------------------------------------------------
@permission_required('dpv_nomencladores.view_prensaescrita', raise_exception=True)
def index_prensaescrita(request):
    prensasescritas = PrensaEscrita.objects.all()
    return render(request,
                  'dpv_nomencladores/list_prensaescrita.html',
                  {'prensasescritas': prensasescritas})


@permission_required('dpv_nomencladores.add_prensaescrita')
def add_prensaescrita(request):
    if request.method == 'POST':
        form = PrensaEscritaForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_prensaescrita')
    else:
        form = PrensaEscritaForm()
    return render(request, 'dpv_nomencladores/form_prensaescrita.html', {'form': form})


@permission_required('dpv_nomencladores.change_prensaescrita')
def update_prensaescrita(request, id_prensaescrita):
    prensaescrita = PrensaEscrita.objects.get(id=id_prensaescrita)
    if request.method == 'POST':
        form = PrensaEscritaForm(request.POST, instance=prensaescrita)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_prensaescrita')
    else:
        form = PrensaEscritaForm(instance=prensaescrita)
    return render(request, 'dpv_nomencladores/form_prensaescrita.html', {'form': form, 'prensaescrita': prensaescrita})


@permission_required('dpv_nomencladores.delete_prensaescrita')
def delete_prensaescrita(request, id_prensaescrita):
    prensaescrita = PrensaEscrita.objects.get(id=id_prensaescrita)
    if request.method == 'POST':
        prensaescrita.perform_log(request=request, af=2)
        prensaescrita.delete()
        return redirect('nomenclador_prensaescrita')
    return render(request,
                  'dpv_nomencladores/delete_prensaescrita.html',
                  {'prensaescrita': prensaescrita})


def autofill_prensaescrita(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            if len(nombre) >= 3:
                prensasescritas = [model_to_dict(mot) for mot in PrensaEscrita.objects.filter(nombre__icontains=nombre)[:10]]
        return JsonResponse(data=prensasescritas, safe=False, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def found_prensaescrita_by_name(request):
    if request.method == 'POST':
        data = dict()
        nombre = request.POST.get('nombre')
        print(nombre)
        if nombre:
            prensaescrita = PrensaEscrita.objects.filter(nombre=nombre).first()
            if prensaescrita:
                data['exist'] = True
                data['prensaescrita'] = model_to_dict(prensaescrita)
            else:
                data['exist'] = False
        return JsonResponse(data=data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# --------------------------------------- Telefono ------------------------------------------------
@permission_required('dpv_nomencladores.view_telefono', raise_exception=True)
def index_telefono(request):
    telefonos = Telefono.objects.all()
    return render(request,
                  'dpv_nomencladores/list_telefono.html',
                  {'telefonos': telefonos})


@permission_required('dpv_nomencladores.add_telefono')
def add_telefono(request):
    if request.method == 'POST':
        form = TelefonoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_telefono')
    else:
        form = TelefonoForm()
    return render(request, 'dpv_nomencladores/form_telefono.html', {'form': form})


@permission_required('dpv_nomencladores.change_telefono')
def update_telefono(request, id_telefono):
    telefono = Telefono.objects.get(id=id_telefono)
    if request.method == 'POST':
        form = TelefonoForm(request.POST, instance=telefono)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_telefono')
    else:
        form = TelefonoForm(instance=telefono)
    return render(request, 'dpv_nomencladores/form_telefono.html', {'form': form, 'telefono': telefono})


@permission_required('dpv_nomencladores.delete_telefono')
def delete_telefono(request, id_telefono):
    telefono = Telefono.objects.get(id=id_telefono)
    if request.method == 'POST':
        telefono.perform_log(request=request, af=2)
        telefono.delete()
        return redirect('nomenclador_telefono')
    return render(request,
                  'dpv_nomencladores/delete_telefono.html',
                  {'telefono': telefono})


def autofill_telefono(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        if numero:
            if len(numero) >= 3:
                telefonos = [model_to_dict(mot) for mot in Telefono.objects.filter(numero__icontains=numero)[:10]]
        return JsonResponse(data=telefonos, safe=False, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def found_telefono_by_number(request):
    if request.method == 'POST':
        data = dict()
        numero = request.POST.get('numero')
        print(numero)
        if numero:
            telefono = Telefono.objects.filter(nombre=numero).first()
            if telefono:
                data['exist'] = True
                data['telefono'] = model_to_dict(telefono)
            else:
                data['exist'] = False
        return JsonResponse(data=data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# --------------------------------------- Email ------------------------------------------------
@permission_required('dpv_nomencladores.view_email', raise_exception=True)
def index_email(request):
    emails = Email.objects.all()
    return render(request,
                  'dpv_nomencladores/list_email.html',
                  {'emails': emails})


@permission_required('dpv_nomencladores.add_email')
def add_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_email')
    else:
        form = EmailForm()
    return render(request, 'dpv_nomencladores/form_email.html', {'form': form})


@permission_required('dpv_nomencladores.change_email')
def update_email(request, id_email):
    email = Email.objects.get(id=id_email)
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=email)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_email')
    else:
        form = EmailForm(instance=email)
    return render(request, 'dpv_nomencladores/form_email.html', {'form': form, 'email': email})


@permission_required('dpv_nomencladores.delete_email')
def delete_email(request, id_email):
    email = Email.objects.get(id=id_email)
    if request.method == 'POST':
        email.perform_log(request=request, af=2)
        email.delete()
        return redirect('nomenclador_telefono')
    return render(request,
                  'dpv_nomencladores/delete_email.html',
                  {'email': email})


def autofill_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        emails = []
        if email:
            if len(email) >= 3:
                emails = [model_to_dict(mot) for mot in Email.objects.filter(email__icontains=email)[:10]]
        return JsonResponse(data=emails, safe=False, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def found_email_by_address(request):
    if request.method == 'POST':
        data = dict()
        email = request.POST.get('email')
        print(email)
        if email:
            found_email = Email.objects.filter(email=email).first()
            if found_email:
                data['exist'] = True
                data['email'] = model_to_dict(found_email)
            else:
                data['exist'] = False
        return JsonResponse(data=data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# --------------------------------------- Organizacion ------------------------------------------------
@permission_required('dpv_nomencladores.view_organizacion', raise_exception=True)
def index_organizacion(request):
    organizaciones = Organizacion.objects.all()
    return render(request,
                  'dpv_nomencladores/list_organizacion.html',
                  {'organizaciones': organizaciones})


@permission_required('dpv_nomencladores.add_organizacion')
def add_organizacion(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_organizacion')
    else:
        form = OrganizationForm()
    return render(request, 'dpv_nomencladores/form_organizacion.html', {'form': form})


@permission_required('dpv_nomencladores.change_organizacion')
def update_organizacion(request, id_organizacion):
    organizacion = Organizacion.objects.get(id=id_organizacion)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organizacion)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_organizacion')
    else:
        form = OrganizationForm(instance=organizacion)
    return render(request, 'dpv_nomencladores/form_organizacion.html', {'form': form, 'organizacion': organizacion})


@permission_required('dpv_nomencladores.delete_organizacion')
def delete_organizacion(request, id_organizacion):
    organizacion = Organizacion.objects.get(id=id_organizacion)
    if request.method == 'POST':
        organizacion.perform_log(request=request, af=2)
        organizacion.delete()
        return redirect('nomenclador_organizacion')
    return render(request,
                  'dpv_nomencladores/delete_organizacion.html',
                  {'organizacion': organizacion})


def autofill_organizacion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            if len(nombre) >= 3:
                organizaciones = [model_to_dict(mot) for mot in Organizacion.objects.filter(nombre__icontains=nombre)[:10]]
        return JsonResponse(data=organizaciones, safe=False, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def found_organizacion_by_name(request):
    if request.method == 'POST':
        data = dict()
        nombre = request.POST.get('nombre')
        print(nombre)
        if nombre:
            organizacion = Organizacion.objects.filter(nombre=nombre).first()
            if organizacion:
                data['exist'] = True
                data['organizacion'] = model_to_dict(organizacion)
            else:
                data['exist'] = False
        return JsonResponse(data=data, status=200)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required()
def create_reponder_a_json(request):
    print(request.method)
    if request.method == 'POST':
        form = RespuestaAQuejaForm(request.POST)
        if form.is_valid():
            resp = form.save(commit=False)
            resp.save_and_log(request=request, af=0)
            data = model_to_dict(resp, fields=['id', 'nombre', ])
            return JsonResponse(data=data, status=201)
    return JsonResponse({"error": "Method not allowed"}, status=405)


# --------------------------------------- Red Social ------------------------------------------------
@permission_required('dpv_nomencladores.view_redsocial', raise_exception=True)
def index_redsocial(request):
    redessoc = RedSocial.objects.all()
    return render(request,
                  'dpv_nomencladores/list_rsocial.html',
                  {'redes_sociales': redessoc})


@permission_required('dpv_nomencladores.add_redsocial')
def add_redsocial(request):
    form = RedSocialForm()
    if request.method == 'POST':
        form = RedSocialForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_gobierno')
    return render(request, 'dpv_nomencladores/form_rsocial.html', {'form': form})


@permission_required('dpv_nomencladores.change_redsocial')
def update_redsocial(request, id_redsoc):
    redsoc = get_object_or_404(RedSocial, id=id_redsoc)
    form = RedSocialForm(instance=redsoc)
    if request.method == 'POST':
        form = RedSocialForm(request.POST, request.FILES, instance=redsoc)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_gobierno')
    return render(request, 'dpv_nomencladores/form_rsocial.html', {'form': form, 'red_social': redsoc})


@permission_required('dpv_nomencladores.delete_redsocial')
def delete_redsocial(request, id_redsoc):
    redsoc = get_object_or_404(RedSocial, id=id_redsoc)
    if request.method == 'POST':
        redsoc.perform_log(request=request, af=2)
        redsoc.delete()
        return redirect('nomenclador_gobierno')
    return render(request,
                  'dpv_nomencladores/delete_rsocial.html',
                  {'red_social': redsoc})


@permission_required('dpv_nomencladores.view_redsocial')
def verify_redsocial(request):
    if request.method == 'GET':
        nombre = dominio = False
        if request.GET.get('nombre'):
            nombre = request.GET.get('nombre')
        if request.GET.get('dominio'):
            dominio = request.GET.get('dominio')
        id = request.GET.get('id')
        if not id:
            id = 0
        if nombre:
            if not RedSocial.objects.filter(nombre__iexact=nombre).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if dominio:
            if not RedSocial.objects.filter(dominio=dominio).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)


# --------------------------------------- Precedencia Web ------------------------------------------------
@permission_required('dpv_nomencladores.view_procedenciaweb', raise_exception=True)
def index_procedenciaweb(request):
    pwebs = ProcedenciaWeb.objects.all()
    return render(request,
                  'dpv_nomencladores/list_pweb.html',
                  {'pwebs': pwebs})


@permission_required('dpv_nomencladores.add_procedenciaweb')
def add_procedenciaweb(request):
    form = ProcedenciaWebForm()
    if request.method == 'POST':
        form = ProcedenciaWebForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('nomenclador_gobierno')
    return render(request, 'dpv_nomencladores/form_pweb.html', {'form': form})


@permission_required('dpv_nomencladores.change_procedenciaweb')
def update_procedenciaweb(request, id_pweb):
    pweb = get_object_or_404(ProcedenciaWeb, id=id_pweb)
    form = ProcedenciaWebForm(instance=pweb)
    if request.method == 'POST':
        form = ProcedenciaWebForm(request.POST, request.FILES, instance=pweb)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('nomenclador_gobierno')
    return render(request, 'dpv_nomencladores/form_rsocial.html', {'form': form, 'pweb': pweb})


@permission_required('dpv_nomencladores.delete_procedenciaweb')
def delete_procedenciaweb(request, id_pweb):
    pweb = get_object_or_404(ProcedenciaWeb, id=id_pweb)
    if request.method == 'POST':
        pweb.perform_log(request=request, af=2)
        pweb.delete()
        return redirect('nomenclador_gobierno')
    return render(request,
                  'dpv_nomencladores/delete_pweb.html',
                  {'pweb': pweb})


@permission_required('dpv_nomencladores.view_procedenciaweb')
def verify_procedenciaweb(request):
    if request.method == 'GET':
        perfil = email = False
        if request.GET.get('perfil'):
            perfil = request.GET.get('perfil')
        if request.GET.get('email'):
            email = request.GET.get('email')
        id = request.GET.get('id')
        red_social = request.GET.get('red_social')
        if not id:
            id = 0
        if not red_social:
            return JsonResponse("", safe=False, status=200)
        if perfil:
            if not ProcedenciaWeb.objects.filter(perfil__iexact=perfil, red_social_id=red_social).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        if email:
            if not ProcedenciaWeb.objects.filter(email=email, red_social_id=red_social).exclude(id=id).exists():
                return JsonResponse("true", safe=False, status=200)
            else:
                return JsonResponse("", safe=False, status=200)
        return JsonResponse("", status=400)
    return JsonResponse("", status=405)

