from datetime import timedelta

from django.contrib.auth.decorators import permission_required
from django.db.models import Count, Manager, Func, Sum
from django.shortcuts import render
from apps.dpv_complaint.models import *
from apps.dpv_complaint.forms import FilterForm


@permission_required('dpv_complaint.view_complaint')
def index_natural_complaint(request):
    index_name = 'Índice de las Quejas'
    elms = Complaint.objects.filter(is_natural=True)
    return render(request, "dpv_complaint/index_complaint_new.html",
                  {'index': elms, 'index_name': index_name, 'natural': True})


def get_elements(cleaned_data, type_complaint):
    elements = Complaint.objects.filter(is_natural=type_complaint)
    if cleaned_data['initial_time']:
        elements = elements.filter(enter_date__gte=cleaned_data['initial_time'])
    if cleaned_data['final_time']:
        elements = elements.filter(enter_date__lte=cleaned_data['final_time'])
    if cleaned_data['municipality']:
        if type_complaint:
            elements = elements.filter(person_natural__municipio=cleaned_data['municipality'])
        else:
            elements = elements.filter(person_juridic__municipio=cleaned_data['municipality'])
    if cleaned_data['days']:
        date = min(timezone.now(), cleaned_data['final_time']) - timedelta(cleaned_data['days'])
        elements = elements.filter(enter_date__gte=date)
    if cleaned_data['status'] and cleaned_data['status'] != 'Seleccione Estado':
        elements = elements.filter(status=cleaned_data['status'])
    return elements


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class MonthSqlite(Func):
    function = 'STRFTIME'
    template = '%(function)s("%%m", %(expressions)s)'
    output_field = models.CharField()


@permission_required('dpv_complaint.view_complaint')
def statistics(request):
    query = Manager.raw("SELECT * FROM \"dpv_complaint_complaint\" GROUP BY \"dpv_complaint_complaint\".\"enter_date\", \"dpv_complaint_complaint\".\"is_natural\"")
    # summary = (Complaint.objects
    #            .annotate(m=MonthSqlite('enter_date'))
    #            .values('m')
    #            .annotate(total=Count('total'))
    #            .order_by())
    s = query.__str__()
    by_month = Complaint.objects.values('enter_date').annotate(natural_count=Count('is_natural'))
    return render(request, "dpv_complaint/statistics_view.html", {'dataset': []})


@permission_required('dpv_complaint.view_complaint')
def search(request, type_complaint):
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            elms = get_elements(form.cleaned_data, type_complaint)
            return render(request, "dpv_complaint/index_complaint_new.html",
                          {'index': elms, 'index_name': 'Elementos filtrados', 'natural': type_complaint})
    else:
        form = FilterForm()
    return render(request, "dpv_complaint/search_form.html", {'form': form, 'form_name': 'Plantilla de Búsqueda'})


@permission_required('dpv_complaint.view_complaint')
def index_juridic_complaint(request):
    index_name = 'Índice de las Quejas'
    elms = Complaint.objects.filter(is_natural=False)
    return render(request, "dpv_complaint/index_complaint_new.html", {'index': elms, 'index_name': index_name})


@permission_required('dpv_complaint.view_complaint')
def index_waiting_for_distribution(request):
    index_name = 'Índice de Quejas en espera de su distribución'
    elms = Complaint.objects.filter(department=None)
    return render(request, "dpv_complaint/index_waiting_for_distribution.html",
                  {'index': elms, 'index_name': index_name})


@permission_required('dpv_complaint.view_complaint')
def index_assigned_to_technician(request, technical_id):
    technical = Technical.objects.get(id=technical_id)
    comp = AssignedToTechnician.objects.filter(technical=technical_id)
    index_name = 'Quejas asignadas al técnico' + technical.profile.datos_personales.nombre + ' ' + \
                 technical.profile.datos_personales.apellidos
    return render(request, "dpv_complaint/index_assigned_to_technical.html",
                  {'index': comp, 'index_name': index_name, 'technical_id': technical_id,
                   'technical_name': technical.profile.datos_personales.nombre + ' ' +
                                     technical.profile.datos_personales.apellidos})


@permission_required('dpv_complaint.view_complaint')
def index_technical(request):
    index_name = 'Índice técnicos'
    technical = Technical.objects.all()
    return render(request, 'dpv_complaint/index_technical.html', {'index': technical, 'index_name': index_name})


@permission_required('dpv_complaint.view_complaint')
def index_finished_complaint(request):
    index_name = 'Índice de Quejas Finalizadas'
    elms = FinishedComplaint.objects.all()
    return render(request, "dpv_complaint/index_finished.html", {'index': elms, 'index_name': index_name})


@permission_required('dpv_complaint.view_complaint')
def index_accepted(request):
    index_name = 'Índice de Quejas Aceptadas'
    elms = Accepted.objects.all()
    return render(request, "dpv_complaint/index_accepted_new.html", {'index': elms, 'index_name': index_name})


@permission_required('dpv_complaint.view_complaint')
def watch_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    person = None
    if not complaint.anonymous:
        if complaint.is_natural:
            person = PersonaNatural.objects.get(id=complaint.person_natural.id)
            pass
        else:
            person = PersonaJuridica.objects.get(id=complaint.person_juridic.id)
    else:
        # TODO Anonymous
        pass
    technical = AssignedToTechnician.objects.filter(complaint=complaint_id)
    return render(request, "dpv_complaint/watch_complaint.html", {'complaint_for_dist': complaint,
                                                                  'person': person,
                                                                  'tech': technical.first()})


@permission_required('dpv_complaint.view_complaint')
def watch_finished(request, finished_id):
    complaint = FinishedComplaint.objects.filter(id=finished_id)
    return render(request, "dpv_complaint/watch_finished.html", {'index': complaint,
                                                                 'index_name': 'Datos queja finalizada'})


@permission_required('dpv_complaint.view_complaint')
def index_accepted_all(request, accepted_id):
    elms = Accepted.objects.filter(id=accepted_id)
    return render(request, 'dpv_complaint/watch_accepted.html', {'index': elms})
