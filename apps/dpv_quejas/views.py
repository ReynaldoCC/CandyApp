from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required, login_required
from .forms import *
from .models import *


@permission_required('dpv_quejass.view_queja', raise_exception=True)
def index(request):
    return render(request, 'dpv_quejas/list.html')

