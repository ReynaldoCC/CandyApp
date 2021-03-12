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


@permission_required('dpv_documento.change_dpvdocumento')
def detail_doc(request, doc_id):
    doc = get_object_or_404(DPVDocumento, pk=doc_id)
    return render(request, 'dpv_documento/dpvdocumento/detail.html', {"doc": doc})


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
