from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.http import JsonResponse
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


#------------------------------------------- Provincia -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_provincia', raise_exception=True)
def index_provincia(request):
    provincias = Provincia.objects.all()
    return render(request, 'dpv_nomencladores/list_provincia.html', {'provincias': provincias})

@permission_required('dpv_nomencladores.add_provincia')
def add_provincia(request):
    if request.method == 'POST':
        form = ProvinciaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_provincia')
    else:
        form = ProvinciaForm()
    return render(request,'dpv_nomencladores/form_provincia.html',{'form':form})


@permission_required('dpv_nomencladores.change_provincia')
def update_provincia(request, id_provincia):
    provincia = Provincia.objects.get(id=id_provincia)
    if request.method == 'GET':
        form = ProvinciaForm(instance=provincia)
    else:
        form = ProvinciaForm(request.POST, instance=provincia)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_provincia')
    return render(request, 'dpv_nomencladores/form_provincia.html', {'form':form, 'provincia':provincia})

@permission_required('dpv_nomencladores.delete_provincia')
def delete_provincia(request, id_provincia):
    provincia = Provincia.objects.get(id=id_provincia)
    if request.method == 'POST':
        provincia.delete()
        return redirect('nomenclador_provincia')
    return render(request, 'dpv_nomencladores/delete_provincia.html', {'provincia':provincia})

#------------------------------------------- Municipio -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_municipio', raise_exception=True)
def index_municipio(request):
    municipios = Municipio.objects.all()
    return render(request, 'dpv_nomencladores/list_municipio.html', {'municipios': municipios})

@permission_required('dpv_nomencladores.add_municipio')
def add_municipio(request):
    if request.method == 'POST':
        form = MunicipioForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_municipio')
    else:
        form = MunicipioForm()
    return render(request,'dpv_nomencladores/form_municipio.html',{'form':form})

@permission_required('dpv_nomencladores.change_municipio')
def update_municipio(request, id_municipio):
    municipio = Municipio.objects.get(id=id_municipio)
    if request.method == 'GET':
        form = MunicipioForm(instance=municipio)
    else:
        form = MunicipioForm(request.POST, instance=municipio)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_municipio')
    return render(request, 'dpv_nomencladores/form_municipio.html', {'form':form, 'municipio':municipio})

@permission_required('dpv_nomencladores.delete_municipio')
def delete_municipio(request, id_municipio):
    municipio = Municipio.objects.get(id=id_municipio)
    if request.method == 'POST':
        municipio.delete()
        return redirect('nomenclador_municipio')
    return render(request, 'dpv_nomencladores/delete_municipio.html', {'municipio':municipio})

#------------------------------------------- ConsejoPopular -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_consejopopular', raise_exception=True)
def index_consejopopular(request):
    consejopopulars = ConsejoPopular.objects.all()
    return render(request, 'dpv_nomencladores/list_consejopopular.html', {'consejopopulars': consejopopulars})

@permission_required('dpv_nomencladores.add_consejopopular')
def add_consejopopular(request):
    if request.method == 'POST':
        form = ConsejoPopularForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_consejopopular')
    else:
        form = ConsejoPopularForm()
    return render(request,'dpv_nomencladores/form_consejopopular.html',{'form':form})

@permission_required('dpv_nomencladores.change_consejopopular')
def update_consejopopular(request, id_consejopopular):
    consejopopular = ConsejoPopular.objects.get(id=id_consejopopular)
    if request.method == 'GET':
        form = ConsejoPopularForm(instance=consejopopular)
    else:
        form = ConsejoPopularForm(request.POST, instance=consejopopular)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_consejopopular')
    return render(request, 'dpv_nomencladores/form_consejopopular.html', {'form':form, 'consejopopular':consejopopular})

@permission_required('dpv_nomencladores.delete_consejopopular')
def delete_consejopopular(request, id_consejopopular):
    consejopopular = ConsejoPopular.objects.get(id=id_consejopopular)
    if request.method == 'POST':
        consejopopular.delete()
        return redirect('nomenclador_consejopopular')
    return render(request, 'dpv_nomencladores/delete_consejopopular.html', {'consejopopular':consejopopular})


#------------------------------------------- Calle -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_calle', raise_exception=True)
def index_calle(request):
    calles = Calle.objects.all()
    return render(request, 'dpv_nomencladores/list_calle.html', {'calles': calles})


@permission_required('dpv_nomencladores.add_calle')
def add_calle(request):
    if request.method == 'POST':
        form = CalleForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_calle')
    else:
        form = CalleForm()
    return render(request, 'dpv_nomencladores/form_calle.html', {'form': form})


@permission_required('dpv_nomencladores.add_calle')
def add_calle_on_user(request):
    data = {}
    if request.method == 'POST':
        form = CalleForm(request.POST or None)
        # print(form)
        if form.is_valid():
            calle = form.save()
            # print(calle)
            data = {'nombre': calle.nombre,
                    'id': calle.id,
                    }
        else:
            data = {
                'errmsg': form.errors
            }
            return JsonResponse(data, status=400)
    return JsonResponse(data)


@permission_required('dpv_nomencladores.add_calle')
def agree_calle(request):
    calleform = CalleForm()
    calle = Calle()
    return render(request, 'dpv_nomencladores/form_calle_async.html', {'form': calleform, 'calle': calle})


@permission_required('dpv_nomencladores.change_calle')
def update_calle(request, id_calle):
    calle = Calle.objects.get(id=id_calle)
    if request.method == 'GET':
        form = CalleForm(instance=calle)
    else:
        form = CalleForm(request.POST, instance=calle)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_calle')
    return render(request, 'dpv_nomencladores/form_calle.html', {'form':form, 'calle':calle})


@permission_required('dpv_nomencladores.delete_calle')
def delete_calle(request, id_calle):
    calle = Calle.objects.get(id=id_calle)
    if request.method == 'POST':
        calle.delete()
        return redirect('nomenclador_calle')
    return render(request, 'dpv_nomencladores/delete_calle.html', {'calle':calle})

#------------------------------------------- Piso -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_piso', raise_exception=True)
def index_piso(request):
    pisos = Piso.objects.all()
    return render(request, 'dpv_nomencladores/list_piso.html', {'pisos': pisos})

@permission_required('dpv_nomencladores.add_piso')
def add_piso(request):
    if request.method == 'POST':
        form = PisoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_piso')
    else:
        form = PisoForm()
    return render(request,'dpv_nomencladores/form_piso.html',{'form':form})


@permission_required('dpv_nomencladores.change_piso')
def update_piso(request, id_piso):
    piso = Piso.objects.get(id=id_piso)
    if request.method == 'GET':
        form = PisoForm(instance=piso)
    else:
        form = PisoForm(request.POST, instance=piso)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_piso')
    return render(request, 'dpv_nomencladores/form_piso.html', {'form':form, 'piso':piso})


@permission_required('dpv_nomencladores.delete_piso')
def delete_piso(request, id_piso):
    piso = Piso.objects.get(id=id_piso)
    if request.method == 'POST':
        piso.delete()
        return redirect('nomenclador_piso')
    return render(request, 'dpv_nomencladores/delete_piso.html', {'piso':piso})


#------------------------------------------- Organismo -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_organismo', raise_exception=True)
def index_organismo(request):
    organismos = Organismo.objects.all()
    return render(request, 'dpv_nomencladores/list_organismo.html', {'organismos': organismos})


@permission_required('dpv_nomencladores.add_organismo')
def add_organismo(request):
    if request.method == 'POST':
        form = OrganismoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_organismo')
    else:
        form = OrganismoForm()
    return render(request,'dpv_nomencladores/form_organismo.html',{'form':form})


@permission_required('dpv_nomencladores.change_organismo')
def update_organismo(request, id_organismo):
    organismo = Organismo.objects.get(id=id_organismo)
    if request.method == 'GET':
        form = OrganismoForm(instance=organismo)
    else:
        form = OrganismoForm(request.POST, instance=organismo)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_organismo')
    return render(request, 'dpv_nomencladores/form_organismo.html', {'form':form, 'organismo':organismo})


@permission_required('dpv_nomencladores.delete_organismo')
def delete_organismo(request, id_organismo):
    organismo = Organismo.objects.get(id=id_organismo)
    if request.method == 'POST':
        organismo.delete()
        return redirect('nomenclador_organismo')
    return render(request, 'dpv_nomencladores/delete_organismo.html', {'organismo':organismo})


#------------------------------------------- Destino -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_destino', raise_exception=True)
def index_destino(request):
    destinos = Destino.objects.all()
    return render(request, 'dpv_nomencladores/list_destino.html', {'destinos': destinos})


@permission_required('dpv_nomencladores.add_destino')
def add_destino(request):
    if request.method == 'POST':
        form = DestinoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_destino')
    else:
        form = DestinoForm()
    return render(request,'dpv_nomencladores/form_destino.html',{'form':form})


@permission_required('dpv_nomencladores.change_destino')
def update_destino(request, id_destino):
    destino = Destino.objects.get(id=id_destino)
    if request.method == 'GET':
        form = DestinoForm(instance=destino)
    else:
        form = DestinoForm(request.POST, instance=destino)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_destino')
    return render(request, 'dpv_nomencladores/form_destino.html', {'form':form, 'destino':destino})


@permission_required('dpv_nomencladores.delete_destino')
def delete_destino(request, id_destino):
    destino = Destino.objects.get(id=id_destino)
    if request.method == 'POST':
        destino.delete()
        return redirect('nomenclador_destino')
    return render(request, 'dpv_nomencladores/delete_destino.html', {'destino':destino})


#------------------------------------------- Concepto -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_concepto', raise_exception=True)
def index_concepto(request):
    conceptos = Concepto.objects.all()
    return render(request, 'dpv_nomencladores/list_concepto.html', {'conceptos': conceptos})


@permission_required('dpv_nomencladores.add_concepto')
def add_concepto(request):
    if request.method == 'POST':
        form = ConceptoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_concepto')
    else:
        form = ConceptoForm()
    return render(request,'dpv_nomencladores/form_concepto.html',{'form':form})


@permission_required('dpv_nomencladores.change_concepto')
def update_concepto(request, id_concepto):
    concepto = Concepto.objects.get(id=id_concepto)
    if request.method == 'GET':
        form = ConceptoForm(instance=concepto)
    else:
        form = ConceptoForm(request.POST, instance=concepto)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_concepto')
    return render(request, 'dpv_nomencladores/form_concepto.html', {'form':form, 'concepto':concepto})


@permission_required('dpv_nomencladores.delete_concepto')
def delete_concepto(request, id_concepto):
    concepto = Concepto.objects.get(id=id_concepto)
    if request.method == 'POST':
        concepto.delete()
        return redirect('nomenclador_concepto')
    return render(request, 'dpv_nomencladores/delete_concepto.html', {'concepto':concepto})


#------------------------------------------- Genero -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_genero', raise_exception=True)
def index_genero(request):
    generos = Genero.objects.all()
    return render(request, 'dpv_nomencladores/list_genero.html', {'generos': generos})


@permission_required('dpv_nomencladores.add_genero')
def add_genero(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_genero')
    else:
        form = GeneroForm()
    return render(request,'dpv_nomencladores/form_genero.html',{'form':form})


@permission_required('dpv_nomencladores.change_genero')
def update_genero(request, id_genero):
    genero = Genero.objects.get(id=id_genero)
    if request.method == 'GET':
        form = GeneroForm(instance=genero)
    else:
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_genero')
    return render(request, 'dpv_nomencladores/form_genero.html', {'form':form, 'genero':genero})

@permission_required('dpv_nomencladores.delete_genero')
def delete_genero(request, id_genero):
    genero = Genero.objects.get(id=id_genero)
    if request.method == 'POST':
        genero.delete()
        return redirect('nomenclador_genero')
    return render(request, 'dpv_nomencladores/delete_genero.html', {'genero':genero})


#------------------------------------------- AreaTrabajo -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_areatrabajo', raise_exception=True)
def index_areatrabajo(request):
    departamentos = AreaTrabajo.objects.all()
    return render(request, 'dpv_nomencladores/list_areatrabajo.html', {'departamentos': departamentos})

@permission_required('dpv_nomencladores.add_areatrabajo')
def add_areatrabajo(request):
    if request.method == 'POST':
        form = AreaTrabajoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_areatrab')
    else:
        form = AreaTrabajoForm()
    return render(request,'dpv_nomencladores/form_areatrabajo.html',{'form':form})

@permission_required('dpv_nomencladores.change_areatrabajo')
def update_areatrabajo(request, id_areatrabajo):
    areatrabajo = AreaTrabajo.objects.get(id=id_areatrabajo)
    if request.method == 'GET':
        form = AreaTrabajoForm(instance=areatrabajo)
    else:
        form = AreaTrabajoForm(request.POST, instance=areatrabajo)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_areatrab')
    return render(request, 'dpv_nomencladores/form_areatrabajo.html', {'form':form, 'areatrabajo':areatrabajo})

@permission_required('dpv_nomencladores.delete_areatrabajo')
def delete_areatrabajo(request, id_areatrabajo):
    areatrabajo = AreaTrabajo.objects.get(id=id_areatrabajo)
    if request.method == 'POST':
        areatrabajo.delete()
        return redirect('nomenclador_areatrab')
    return render(request, 'dpv_nomencladores/delete_areatrabajo.html', {'areatrabajo':areatrabajo})

#------------------------------------------- CentroTrabajo -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_centrotrabajo', raise_exception=True)
def index_centrotrabajo(request):
    unidades = CentroTrabajo.objects.all()
    return render(request, 'dpv_nomencladores/list_centrotrabajo.html', {'unidades': unidades})

@permission_required('dpv_nomencladores.add_centrotrabajo')
def add_centrotrabajo(request):
    if request.method == 'POST':
        form = CentroTrabajoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_centrab')
    else:
        form = CentroTrabajoForm()

    return render(request,'dpv_nomencladores/form_centrotrabajo.html',{'form':form})

@permission_required('dpv_nomencladores.change_centrotrabajo')
def update_centrotrabajo(request, id_centrotrabajo):
    centrotrabajo = CentroTrabajo.objects.get(id=id_centrotrabajo)
    if request.method == 'GET':
        form = CentroTrabajoForm(instance=centrotrabajo)
    else:
        form = CentroTrabajoForm(request.POST, instance=centrotrabajo)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_centrab')
    return render(request, 'dpv_nomencladores/form_centrotrabajo.html', {'form':form, 'centrotrabajo':centrotrabajo})

@permission_required('dpv_nomencladores.delete_centrotrabajo')
def delete_centrotrabajo(request, id_centrotrabajo):
    centrotrabajo = CentroTrabajo.objects.get(id=id_centrotrabajo)
    if request.method == 'POST':
        centrotrabajo.delete()
        return redirect('nomenclador_centrab')
    return render(request, 'dpv_nomencladores/delete_centrotrabajo.html', {'centrotrabajo':centrotrabajo})

#------------------------------------------- CodificadorAsunto -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_codificadorasunto', raise_exception=True)
def index_codificadorasunto(request):
    codificadorasuntos = CodificadorAsunto.objects.all()
    return render(request, 'dpv_nomencladores/list_codificadorasunto.html', {'codificadorasuntos': codificadorasuntos})

@permission_required('dpv_nomencladores.add_codificadorasunto')
def add_codificadorasunto(request):
    if request.method == 'POST':
        form = CodificadorAsuntoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_codificadorasunto')
    else:
        form = CodificadorAsuntoForm()
    return render(request,'dpv_nomencladores/form_codificadorasunto.html',{'form':form})


@permission_required('dpv_nomencladores.change_codificadorasunto')
def update_codificadorasunto(request, id_codificadorasunto):
    codificadorasunto = CodificadorAsunto.objects.get(id=id_codificadorasunto)
    if request.method == 'GET':
        form = CodificadorAsuntoForm(instance=codificadorasunto)
    else:
        form = CodificadorAsuntoForm(request.POST, instance=codificadorasunto)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_codificadorasunto')
    return render(request, 'dpv_nomencladores/form_codificadorasunto.html', {'form':form, 'codificadorasunto':codificadorasunto})

@permission_required('dpv_nomencladores.delete_codificadorasunto')
def delete_codificadorasunto(request, id_codificadorasunto):
    codificadorasunto = CodificadorAsunto.objects.get(id=id_codificadorasunto)
    if request.method == 'POST':
        codificadorasunto.delete()
        return redirect('nomenclador_codificadorasunto')
    return render(request, 'dpv_nomencladores/delete_codificadorasunto.html', {'codificadorasunto':codificadorasunto})

#------------------------------------------- TipoQueja -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_tipoqueja', raise_exception=True)
def index_tipoqueja(request):
    tipoquejas = TipoQueja.objects.all()
    return render(request, 'dpv_nomencladores/list_tipoqueja.html', {'tipoquejas': tipoquejas})

@permission_required('dpv_nomencladores.add_tipoqueja')
def add_tipoqueja(request):
    if request.method == 'POST':
        form = TipoQuejaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_tipoqueja')
    else:
        form = TipoQuejaForm()
    return render(request,'dpv_nomencladores/form_tipoqueja.html',{'form':form})


@permission_required('dpv_nomencladores.change_tipoqueja')
def update_tipoqueja(request, id_tipoqueja):
    tipoqueja = TipoQueja.objects.get(id=id_tipoqueja)
    if request.method == 'GET':
        form = TipoQuejaForm(instance=tipoqueja)
    else:
        form = TipoQuejaForm(request.POST, instance=tipoqueja)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_tipoqueja')
    return render(request, 'dpv_nomencladores/form_tipoqueja.html', {'form':form, 'tipoqueja':tipoqueja})

@permission_required('dpv_nomencladores.delete_tipoqueja')
def delete_tipoqueja(request, id_tipoqueja):
    tipoqueja = TipoQueja.objects.get(id=id_tipoqueja)
    if request.method == 'POST':
        tipoqueja.delete()
        return redirect('nomenclador_tipoqueja')
    return render(request, 'dpv_nomencladores/delete_tipoqueja.html', {'tipoqueja':tipoqueja})

#------------------------------------------- Procedencia -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_procedencia', raise_exception=True)
def index_procedencia(request):
    procedencias = Procedencia.objects.all()
    return render(request, 'dpv_nomencladores/list_procedencia.html', {'procedencias': procedencias})

@permission_required('dpv_nomencladores.add_procedencia')
def add_procedencia(request):
    if request.method == 'POST':
        form = ProcedenciaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_procedencia')
    else:
        form = ProcedenciaForm()
    return render(request,'dpv_nomencladores/form_procedencia.html',{'form':form})


@permission_required('dpv_nomencladores.change_procedencia')
def update_procedencia(request, id_procedencia):
    procedencia = Procedencia.objects.get(id=id_procedencia)
    if request.method == 'GET':
        form = ProcedenciaForm(instance=procedencia)
    else:
        form = ProcedenciaForm(request.POST, instance=procedencia)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_procedencia')
    return render(request, 'dpv_nomencladores/form_procedencia.html', {'form':form, 'procedencia':procedencia})

@permission_required('dpv_nomencladores.delete_procedencia')
def delete_procedencia(request, id_procedencia):
    procedencia = Procedencia.objects.get(id=id_procedencia)
    if request.method == 'POST':
        procedencia.delete()
        return redirect('nomenclador_procedencia')
    return render(request, 'dpv_nomencladores/delete_procedencia.html', {'procedencia':procedencia})

#------------------------------------------- TipoProcedencia -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_tipoprocedencia', raise_exception=True)
def index_tipoprocedencia(request):
    tipoprocedencias = TipoProcedencia.objects.all()
    return render(request, 'dpv_nomencladores/list_tipoprocedencia.html', {'tipoprocedencias': tipoprocedencias})

@permission_required('dpv_nomencladores.add_tipoprocedencia')
def add_tipoprocedencia(request):
    if request.method == 'POST':
        form = TipoProcedenciaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_tipoprocedencia')
    else:
        form = TipoProcedenciaForm()
    return render(request,'dpv_nomencladores/form_tipoprocedencia.html',{'form':form})


@permission_required('dpv_nomencladores.change_tipoprocedencia')
def update_tipoprocedencia(request, id_tipoprocedencia):
    tipoprocedencia = TipoProcedencia.objects.get(id=id_tipoprocedencia)
    if request.method == 'GET':
        form = TipoProcedenciaForm(instance=tipoprocedencia)
    else:
        form = TipoProcedenciaForm(request.POST, instance=tipoprocedencia)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_tipoprocedencia')
    return render(request, 'dpv_nomencladores/form_tipoprocedencia.html', {'form':form, 'tipoprocedencia':tipoprocedencia})

@permission_required('dpv_nomencladores.delete_tipoprocedencia')
def delete_tipoprocedencia(request, id_tipoprocedencia):
    tipoprocedencia = TipoProcedencia.objects.get(id=id_tipoprocedencia)
    if request.method == 'POST':
        tipoprocedencia.delete()
        return redirect('nomenclador_tipoprocedencia')
    return render(request, 'dpv_nomencladores/delete_tipoprocedencia.html', {'tipoprocedencia':tipoprocedencia})

#------------------------------------------- Estado -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_estado', raise_exception=True)
def index_estado(request):
    estados = Estado.objects.all()
    return render(request, 'dpv_nomencladores/list_estado.html', {'estados': estados})

@permission_required('dpv_nomencladores.add_estado')
def add_estado(request):
    if request.method == 'POST':
        form = EstadoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_estado')
    else:
        form = EstadoForm()
    return render(request,'dpv_nomencladores/form_estado.html',{'form':form})


@permission_required('dpv_nomencladores.change_estado')
def update_estado(request, id_estado):
    estado = Estado.objects.get(id=id_estado)
    if request.method == 'GET':
        form = EstadoForm(instance=estado)
    else:
        form = EstadoForm(request.POST, instance=estado)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_estado')
    return render(request, 'dpv_nomencladores/form_estado.html', {'form':form, 'estado':estado})

@permission_required('dpv_nomencladores.delete_estado')
def delete_estado(request, id_estado):
    estado = Estado.objects.get(id=id_estado)
    if request.method == 'POST':
        estado.delete()
        return redirect('nomenclador_estado')
    return render(request, 'dpv_nomencladores/delete_estado.html', {'estado':estado})

#------------------------------------------- ClasificacionRespuesta -----------------------------------------------------------------
@permission_required('dpv_nomencladores.view_clasificacionrespuesta', raise_exception=True)
def index_clasificacionrespuesta(request):
    clasificacionrespuestas = ClasificacionRespuesta.objects.all()
    return render(request, 'dpv_nomencladores/list_clasificacionrespuesta.html', {'clasificacionrespuestas': clasificacionrespuestas})

@permission_required('dpv_nomencladores.add_clasificacionrespuesta')
def add_clasificacionrespuesta(request):
    if request.method == 'POST':
        form = ClasificacionRespuestaForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_clasificacionrespuesta')
    else:
        form = ClasificacionRespuestaForm()
    return render(request,'dpv_nomencladores/form_clasificacionrespuesta.html',{'form':form})


@permission_required('dpv_nomencladores.change_clasificacionrespuesta')
def update_clasificacionrespuesta(request, id_clasificacionrespuesta):
    clasificacionrespuesta = ClasificacionRespuesta.objects.get(id=id_clasificacionrespuesta)
    if request.method == 'GET':
        form = ClasificacionRespuestaForm(instance=clasificacionrespuesta)
    else:
        form = ClasificacionRespuestaForm(request.POST, instance=clasificacionrespuesta)
        if form.is_valid():
            form.save()
        return redirect('nomenclador_clasificacionrespuesta')
    return render(request, 'dpv_nomencladores/form_clasificacionrespuesta.html', {'form':form, 'clasificacionrespuesta':clasificacionrespuesta})

@permission_required('dpv_nomencladores.delete_clasificacionrespuesta')
def delete_clasificacionrespuesta(request, id_clasificacionrespuesta):
    clasificacionrespuesta = ClasificacionRespuesta.objects.get(id=id_clasificacionrespuesta)
    if request.method == 'POST':
        clasificacionrespuesta.delete()
        return redirect('nomenclador_clasificacionrespuesta')
    return render(request, 'dpv_nomencladores/delete_clasificacionrespuesta.html', {'clasificacionrespuesta':clasificacionrespuesta})