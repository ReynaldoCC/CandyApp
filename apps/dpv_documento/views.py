from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import TipoDPVDocumento, DPVDocumento
from .forms import TipoDPVDocumentoForm, DPVDocumentoForm


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


def list_docs(request):
    docs = DPVDocumento.objects.all()
    return render(request, "dpv_documento/dpvdocumento/list.html", {"docs": docs})


def create_doc(request):

    if request.method == 'POST':

        form = DPVDocumentoForm(request.POST)

        if form.is_valid():
            model = form.save(commit=False)
            model.registrado_por = request.user
            model.fecha_termino
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