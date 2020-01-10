from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from apps.dpv_complaint.forms import *
from apps.dpv_complaint.models import *


@permission_required('dpv_complaint.change_complaint')
def assign_department(request, complaint_id):
    form_name = "Asignar Departamento"
    if request.method == 'POST':
        form = AssignDepartmentForm(request.POST)
        if form.is_valid():
            args = form.fields['department'].queryset.first()
            Complaint.objects.filter(id=complaint_id).update(department=args,
                                                                         assigned_to_department_date=timezone.now())
            history = HistoryComplaint(complaint=Complaint.objects.get(id=complaint_id), current_status='Esperando Asignación')

            history.save()

            CurrentComplaint.objects.filter(complaint=complaint_id).update(
                current_status=history.current_status)

            return redirect(reverse_lazy('index_natural_complaint'))
    else:
        form = AssignDepartmentForm()
    return render(request, 'dpv_complaint/single_form.html', {'form': form, 'form_name': form_name})

