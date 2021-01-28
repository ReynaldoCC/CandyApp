from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from apps.dpv_nomencladores.models import TipoProcedencia, Procedencia, PrensaEscrita, Telefono, Email, \
    Organizacion
from apps.dpv_persona.models import PersonaNatural, PersonaJuridica
from apps.dpv_quejas.forms import QPrensaEscritaForm, AQPersonaNaturalForm, QTelefonoForm, QEmailForm, \
    QPersonaJuridicaForm, QOrganizationForm, QAnonimoForm
from .models import TipoDPVDocumento, DPVDocumento
from django.forms.models import model_to_dict
from .forms import TipoDPVDocumentoForm, DPVDocumentoForm, DVPDocumentoEditForm, DVPDocumentoFechaEntregaForm, DocsProcedenciaForm


# Create your views here.
def list_typedocs(request):
    typedocs = TipoDPVDocumento.objects.all()
    return render(request, "dpv_documento/tipodpvdocumento/list.html", {"typedocs": typedocs})


@permission_required('dpv_documento.add_tipodpvdocumento')
def create_typedocs(request):
    if request.method == 'POST':
        form = TipoDPVDocumentoForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=0)
        return redirect('list_typedocs')
    else:
        form = TipoDPVDocumentoForm()
    return render(request, 'dpv_documento/tipodpvdocumento/form.html', {'form': form})


@permission_required('dpv_documento.change_tipodpvdocumento')
def update_typedocs(request, typedoc_id):
    typedoc = TipoDPVDocumento.objects.get(id=typedoc_id)
    if request.method == 'POST':
        form = TipoDPVDocumentoForm(request.POST, instance=typedoc)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('list_typedocs')
    else:
        form = TipoDPVDocumentoForm(instance=typedoc)
    return render(request, 'dpv_documento/tipodpvdocumento/form.html', {'form': form, 'typedoc': typedoc})


@permission_required('dpv_documento.delete_tipodpvdocumento')
def delete_typedocs(request, typedoc_id):
    typedoc = TipoDPVDocumento.objects.get(id=typedoc_id)
    if request.method == 'POST':
        typedoc.perform_log(request=request, af=2)
        typedoc.delete()
        return redirect('list_typedocs')
    return render(request, 'dpv_documento/tipodpvdocumento/delete.html', {'typedoc': typedoc})


@login_required()
def typedoc_filter_con_respuesta(request, typedoc_id):

    try:
        typedoc = TipoDPVDocumento.objects.get(pk=typedoc_id)
    except:
        return JsonResponse({"error": "Invalid id value"})
    else:
        return JsonResponse({'display':typedoc.con_respuesta}, safe=False, status=200)


@permission_required('dpv_documento.view_dpvdocumento')
def list_docs(request):
    docs = DPVDocumento.objects.all()
    return render(request, "dpv_documento/dpvdocumento/list.html", {"docs": docs})


@permission_required('dpv_documento.add_dpvdocumento')
def create_doc(request):

    if request.method == 'POST':
        form = DPVDocumentoForm(request.POST, request.FILES)

        if form.is_valid():
            model = form.save(commit=False)
            model.registrado_por = request.user
            model.save()
            messages.success(request, "Documento agregado satisfactoriamente.")
            return redirect(reverse_lazy('list_docs'))
        else:
            messages.error(request, form.errors)
    else:
        form = DPVDocumentoForm()

    return render(
        request,
        'dpv_documento/dpvdocumento/create.html',
        {
            'form': form
        }
    )


@permission_required('dpv_documento.change_dpvdocumento')
def update_doc(request, doc_id):
    doc = DPVDocumento.objects.get(id=doc_id)

    if request.method == 'POST':
        form = DVPDocumentoEditForm(request.POST, instance=doc)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        return redirect('list_docs')
    else:
        form = DVPDocumentoEditForm(instance=doc)
    return render(request, 'dpv_documento/dpvdocumento/update.html', {'form': form, 'doc': doc})


@permission_required('dpv_documento.change_dpvdocumento')
def setdate_doc(request, doc_id):
    doc = DPVDocumento.objects.get(id=doc_id)

    if request.method == 'POST':
        form = DVPDocumentoFechaEntregaForm(request.POST, instance=doc)
        if form.is_valid():
            model = form.save()
            model.perform_log(request=request, af=1)
        else:
            print(form.errors)
        return redirect('list_docs')
    else:
        form = DVPDocumentoFechaEntregaForm(instance=doc)
    return render(request, 'dpv_documento/dpvdocumento/setdatemodal_dpvdocumento.html', {'form': form, 'doc': doc})


@permission_required('dpv_documento.delete_dpvdocumento')
def delete_docs(request, doc_id):
    doc = DPVDocumento.objects.get(id=doc_id)
    if request.method == 'POST':
        doc.perform_log(request=request, af=2)
        doc.delete()
        return redirect('list_docs')
    return render(request, 'dpv_documento/dpvdocumento/delete.html', {'doc': doc})


@permission_required('dpv_nomencladores.add_procedencia')
def create_procedencia(request):
    form = DocsProcedenciaForm(prefix='procedencia')
    peform = QPrensaEscritaForm(prefix='pe', empty_permitted=True, use_required_attribute=False)
    aqform = AQPersonaNaturalForm(prefix='person_procedence', empty_permitted=True, use_required_attribute=False)
    tform = QTelefonoForm(prefix='telefono', empty_permitted=True, use_required_attribute=False)
    eform = QEmailForm(prefix='email', empty_permitted=True, use_required_attribute=False)
    pjform = QPersonaJuridicaForm(prefix='empresa', empty_permitted=True, use_required_attribute=False)
    oform = QOrganizationForm(prefix='organiza', empty_permitted=True, use_required_attribute=False)


    if request.method == 'POST':
        data = {}
        status = 200

        procedence_form = QAnonimoForm()

        if request.POST.get('pe-nombre'):
            pe = PrensaEscrita.objects.filter(nombre=request.POST.get('pe-nombre'))
            if pe:
                procedence_form = peform = QPrensaEscritaForm(request.POST, prefix='pe', use_required_attribute=False,
                                                              instance=pe.first(), empty_permitted=True)
            else:
                procedence_form = peform = QPrensaEscritaForm(request.POST, prefix='pe',
                                                              use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('person_procedence-ci') and request.POST.get('person_procedence-nombre'):
            pn = PersonaNatural.objects.filter(ci=request.POST.get('person_procedence-ci'))
            if pn:
                procedence_form = aqform = AQPersonaNaturalForm(request.POST, prefix='person_procedence',
                                                                use_required_attribute=False,
                                                                instance=pn.first(), empty_permitted=True)
            else:
                procedence_form = aqform = AQPersonaNaturalForm(request.POST, prefix='person_procedence',
                                                                use_required_attribute=False, empty_permitted=True)
        elif request.POST.get('telefono-numero'):
            tel = Telefono.objects.filter(numero=request.POST.get('telefono-numero'))
            if tel:
                procedence_form = tform = QTelefonoForm(request.POST, prefix='telefono', use_required_attribute=False,
                                                        instance=tel.first(), empty_permitted=True)
            else:
                procedence_form = tform = QTelefonoForm(request.POST, prefix='telefono', use_required_attribute=False,
                                                        empty_permitted=True)
        elif request.POST.get('email-email'):
            ema = Email.objects.filter(email=request.POST.get('email-email'))
            if ema:
                procedence_form = QEmailForm(request.POST, prefix='email', use_required_attribute=False,
                                                     instance=ema.first(), empty_permitted=True)
            else:
                procedence_form = QEmailForm(request.POST, prefix='email', use_required_attribute=False,
                                                     empty_permitted=True)
        elif request.POST.get('empresa-nombre') and request.POST.get('empresa-codigo_nit') and request.POST.get('empresa-codigo_reuup'):
            pj = PersonaJuridica.objects.filter(codigo_nit=request.POST.get('empresa-codigo_nit'),
                                                codigo_reuup=request.POST.get('empresa-codigo_reuup'),
                                                nombre=request.POST.get('empresa-nombre'))
            if pj:
                procedence_form = pjform = QPersonaJuridicaForm(request.POST, prefix='empresa',
                                                                instance=pj.first(), empty_permitted=True,
                                                                use_required_attribute=False)
            else:
                procedence_form = pjform = QPersonaJuridicaForm(request.POST, prefix='empresa', empty_permitted=True,
                                                                use_required_attribute=False)
        elif request.POST.get('organiza-nombre'):
            org = Organizacion.objects.filter(nombre=request.POST.get('organiza-nombre')[0])
            if org:
                procedence_form = oform = QOrganizationForm(request.POST, prefix='organiza',
                                                            use_required_attribute=False,
                                                            instance=org.first(), empty_permitted=True)
            else:
                procedence_form = oform = QOrganizationForm(request.POST, prefix='organiza',
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
            data = model_to_dict(proc)
            return JsonResponse(data=data, status=status)
        else:
            data['errors'] = form.errors
            status = 400
        return JsonResponse(data=data, status=status)

    return render(
        request,
        'dpv_documento/dpvdocumento/formodal_procedencia.html',
        {
            'form': form,
            'pjform': pjform,
            'tform': tform,
            'eform': eform,
            'oform': oform,
            'peform': peform,
            'aqform': aqform
        }
    )


@login_required()
def valid_procedencia_in_personal(request, procedencia_id):

    try:
        procedencia = Procedencia.objects.get(pk=procedencia_id)
    except:
        return JsonResponse({"error": "Invalid id value"})
    else:
        return JsonResponse({'display': True if procedencia.tipo.nombre in ("Personal") else False}, safe=False, status=200)