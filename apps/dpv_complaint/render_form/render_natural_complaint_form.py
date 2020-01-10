from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from apps.dpv_complaint.forms import *
from apps.dpv_complaint.models import *
from apps.dpv_persona.forms import PersonaNaturalForm


def check_natural_person(ci):
    # Check if exist a person for the CI
    by_ci = PersonaNatural.objects.filter(ci=ci)
    # Check if exist a person for the email
    return by_ci.exists()


@permission_required('dpv_complaint.add_complaint')
def form_natural_complaint(request, person_id):
    form_name = "Datos de Queja Natural"
    if request.method == "POST":
        form_complaint = ComplaintForm(request.POST)
        if form_complaint.is_valid():
            complaint = form_complaint.save(commit=False)
            complaint.is_natural = True
            complaint.person_natural = PersonaNatural.objects.get(id=person_id)
            complaint.enter_date = timezone.now()
            complaint.department = None
            complaint.save()
            p = WaitingForDistribution()
            p.complaint = complaint
            p.enter_date = timezone.now()
            p.save()

            history = HistoryComplaint()
            history.complaint = complaint
            history.date_of_status = p.enter_date
            history.current_status = 'Pendiente'
            history.save()

            current_complaint = CurrentComplaint()
            current_complaint.complaint = complaint
            current_complaint.current_status = history.current_status
            current_complaint.save()

            return redirect(reverse_lazy('index_natural_complaint'))
    else:
        form_complaint = ComplaintForm()
    return render(request, "dpv_complaint/form_complaint.html",
                  {'form': form_complaint, 'form_name': form_name})


@permission_required('dpv_complaint.add_complaint')
def middle_form_natural_complaint(request, person_id):
    complaints = Complaint.objects.all().filter(person_natural=person_id)
    if complaints.exists():
        return render(request, "dpv_complaint/index_by_person.html", {'index': complaints,
                                                                      'index_name': 'Obtener Persona por ID',
                                                                      'person': person_id,
                                                                      'is_natural': True})
    else:
        return redirect(reverse_lazy('add_natural_complaint', args=[person_id]))
    pass


@permission_required('dpv_complaint.add_complaint')
def form_person_for_complaint(request):
    form_name = "Insertar persona natural"
    if request.method == "POST":
        form_natural = PersonaNaturalForm(request.POST)
        ci = form_natural.data.get('ci')
        if check_natural_person(ci):
            person = PersonaNatural.objects.get(ci=ci)
            return redirect(reverse_lazy('complaints_by_person', args=[person.id]))

        elif form_natural.is_valid():
            person = form_natural.save()
            return redirect(reverse_lazy('add_natural_complaint', args=[person.id]))

    else:
        form_natural = PersonaNaturalForm()
    return render(request, "dpv_complaint/form_natural_person.html",
                  {'form': form_natural, 'form_name': form_name})
