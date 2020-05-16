from django.shortcuts import render
from .models import DPVDocumento


# Create your views here.
def index(request):
    docs = DPVDocumento.objects.all()
    return render(request, "dpv_documento/dpvdocumento/list.html", {"docs": docs})
