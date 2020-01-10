# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import Permission, User
from django.utils import formats
import datetime


MESES = {
    1:"Enero",
    2:"Febrero",
    3:"Marzo",
    4:"Abril",
    5:"Mayo",
    6:"Junio",
    7:"Julio",
    8:"Agosto",
    9:"Septiembre",
    10:"Octubre",
    11:"Noviembre",
    12:"Diciembre",
}


class Frecuencia(models.Model):
    name = models.CharField(max_length=255)
    days = models.IntegerField()

    class Meta:
        verbose_name_plural = 'frecuencias'

    def __str__(self):
        return self.name


class TipoEvento(models.Model):
    type = models.CharField(max_length=255)
    frecuencia = models.ForeignKey(Frecuencia,null=True, blank=True, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'tipos de eventos'

    def __str__(self):
        return self.type


class Evento(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    date_programed = models.DateTimeField()
    site = models.CharField(max_length=255)
    month = models.IntegerField()
    is_extraordinario = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    date_done = models.DateTimeField(blank=True,null=True)

    class Meta:
        verbose_name_plural = 'eventos'

    def __str__(self):
        return "{}({})".format(self.type.type, MESES[self.month])

    @property
    def get_month(self):
        return MESES[int(self.month)]

    @property
    def get_datetime_programed(self):
        string = ''
        if self.date_programed not in (None, ''):
            try:
                year, month, day, hour, minute = self.date_programed.year, self.date_programed.month, self.date_programed.day, self.date_programed.hour, self.date_programed.minute
            except:
                year, month, day = self.date_programed.split('-')
                day, time = day.split(' ')
                hour, minute = time.split(':')
            finally:
                string = str(format(formats.date_format(datetime.datetime(int(year), int(month), int(day), int(hour), int(minute)),'DATETIME_FORMAT')))

        return string

    @property
    def get_date_programed(self):
        string = ''
        if self.date_programed not in (None, ''):
            try:
                year, month, day = self.date_programed.year, self.date_programed.month, self.date_programed.day
            except:
                year, month, day = self.date_programed.split('-')
                day, time = day.split(' ')
            finally:
                string = str(format(formats.date_format(datetime.date(int(year), int(month), int(day)))))

        return string

    @property
    def get_time_programed(self):
        string = ''
        if self.date_programed not in (None, ''):
            try:
                hour, minute = self.date_programed.hour, self.date_programed.minute
            except:
                date, time = self.date_programed.split(' ')
                hour, minute = time.split(':')
            finally:
                string = str(format(formats.time_format(datetime.time(int(hour), int(minute)), "h:i A")))

        return string

    @property
    def get_is_extraordinario(self):
        string = 'Ordinario'

        if self.is_extraordinario:
            string = 'Extraordinario'

        return string

    @property
    def in_time(self):
        return self.date_programed > timezone.now()


def generate_code_acta():
    return "{}/{}".format(len(Acta.objects.all()),timezone.now().year)


def generate_code_acuerdo():
    return "{}/{}".format(len(Acuerdo.objects.all()),timezone.now().year)


class Acta(models.Model):
    event = models.OneToOneField(Evento, on_delete=models.CASCADE)
    code = models.CharField(max_length=25, default=generate_code_acta)
    body = models.TextField()
    date_created = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'actas'


class Acuerdo(models.Model):
    code = models.CharField(max_length=25,default=generate_code_acuerdo)
    event = models.ForeignKey(Evento, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=255)
    date_finish = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    date_done = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'acuerdos'

    @property
    def state(self):
        state = ''

        if self.is_done:
            state = 'Cumplido'
        elif self.date_finish < timezone.now():
            state = 'Incumplido'
        else:
            state = 'En Proceso'

        return state


class TemaEvento(models.Model):
    asunto = models.CharField(max_length=255)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    es_sugerido = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'temas de evento'


class ResponsableAcuerdo(models.Model):
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    acuerdo = models.ForeignKey(Acuerdo, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'responsables'


class RespuestaAcuerdo(models.Model):
    responsable = models.ForeignKey(ResponsableAcuerdo, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'respuestaacuerdos'
