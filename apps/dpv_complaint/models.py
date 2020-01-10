# from apps.dpv_nomencladores.models import AreaTrabajo, Municipio
from apps.dpv_perfil.models import Perfil
from django.utils import timezone
from apps.dpv_persona.models import *

stat = {
    ('Pendiente', 'P'),
    ('Esperando Asignación', 'EA'),
    ('Esperando Respuesta de Técnico', 'ERT'),
    ('Esperando aceptación del jefe', 'EAJ'),
    ('Finalizada', 'F'),
}
stat_history = {
    ('Pendiente', 'Pendiente'),
    ('Esperando Asignación', 'Esperando Asignación'),
    ('Esperando Respuesta de Técnico', 'Esperando Respuesta de Técnico'),
    ('Esperando aceptación del jefe', 'Esperando aceptación del jefe'),
    ('Finalizada', 'Finalizada'),
}

ans = {
    ('S', "Solución o Resuelto"),
    ('PS', 'Pendiente de Solución'),
    ('PR', 'Pendiente de Respuesta'),
    ('ECNS', 'Explicada Causa de no Solución'),
    ('Trámite', 'Trámite')
}


class Complaint(models.Model):
    origin = models.CharField(max_length=50, default='', blank=True, verbose_name='Procedencia')
    body = models.TextField(max_length=1000, verbose_name='Cuerpo de la queja')
    topic = models.CharField(max_length=200, verbose_name='Asunto')
    number = models.CharField(max_length=15, unique=True, verbose_name='Número')
    status = models.CharField(choices=stat, default='Pendiente', max_length=20)
    enter_date = models.DateTimeField(default=timezone.now)
    assigned_to_department_date = models.DateTimeField(blank=True, default=timezone.now)
    is_natural = models.BooleanField(default=True)
    person_natural = models.ForeignKey(PersonaNatural, related_name='person_natural', on_delete=False,
                                       blank=True, null=True)
    person_juridic = models.ForeignKey(PersonaJuridica, related_name='person_juridic', on_delete=models.CASCADE,
                                       blank=True, null=True)
    department = models.ForeignKey(AreaTrabajo, related_name='department', on_delete=False, null=True,
                                   verbose_name='Departamento')
    anonymous = models.BooleanField(default=False)
    expiration_time = models.IntegerField(default=60)
    reference = models.CharField(default='', max_length=50, blank=True, verbose_name='Referencia')

    def __str__(self):
        return '{}'.format(self.topic)


class PopularCouncil(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.name)


class Approach(models.Model):
    reference_number = models.IntegerField()
    municipality = models.ForeignKey(Municipio, on_delete=False, default='', blank=True)
    popular_council = models.ForeignKey(PopularCouncil, on_delete=False)
    entity = models.ForeignKey(PersonaJuridica, on_delete=False)
    topic = models.CharField(max_length=200, verbose_name='Asunto')
    text = models.CharField(max_length=1000)
    made_by = models.ForeignKey(PersonaNatural, related_name='approach_made_by', on_delete=False, blank=True)
    expiration_time = models.IntegerField(default=30)
    # address of the one how make the approach


class Technical(models.Model):
    profile = models.ForeignKey(Perfil, on_delete=False, related_name='profile')

    def __str__(self):
        return '{}'.format(self.profile.datos_personales.nombre + ' ' + self.profile.datos_personales.apellidos)


class WaitingForDistribution(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=False)
    enter_date = models.DateTimeField(default=timezone.now)


class AssignedToTechnician(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=False)
    technical = models.ForeignKey(Technical, on_delete=models.CASCADE)
    enter_date = models.DateTimeField(default=timezone.now)
    assigned_by = models.ForeignKey(Perfil, on_delete=False, default=1)


class FinishedComplaint(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=False)
    technical = models.ForeignKey(Technical, on_delete=False)
    technical_args = models.TextField()
    enter_date = models.DateTimeField(default=timezone.now)


class Accepted(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=False)
    technical_work_in_complaint = models.ForeignKey(Technical, on_delete=False, default=1,
                                                    related_name='technical_accepted')
    technical_args = models.TextField()
    final_args = models.TextField()
    finished_date = models.DateTimeField(default=timezone.now)
    boss_accepted = models.ForeignKey(Perfil, on_delete=False, default=False, related_name='boss_accepted')
    answer = models.CharField(choices=ans, default='S', max_length=100)


class HistoryComplaint(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=False, blank=True, null=True)
    technical = models.ForeignKey(Technical, on_delete=False, related_name='technical_history', null=True, blank=True)
    boss = models.ForeignKey(Perfil, on_delete=False, blank=True, null=True, related_name='boss')
    assigned_by = models.ForeignKey(Perfil, on_delete=False, blank=True, null=True, related_name='assigned_by')
    technical_args = models.TextField()
    boss_args = models.TextField()
    final_args = models.TextField(default='')
    boss_answer = models.CharField(choices=ans, default='S', max_length=20, blank=True)
    date_of_status = models.DateTimeField(auto_now_add=True)
    current_status = models.CharField(default='Pendiente', choices=stat_history, max_length=200)
    approach = models.ForeignKey(Approach, on_delete=False, blank=True, null=True)
    is_complaint = models.BooleanField(default=True)


class CurrentComplaint(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=False)
    current_status = models.CharField(max_length=100, default='Pendiente', choices=stat_history)
