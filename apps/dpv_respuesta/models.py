from django.db import models
from apps.dpv_nomencladores.models import *
from apps.dpv_perfil.models import *

class Respuesta(models.Model):
    texto = models.TextField(max_length=1000, default='', blank=True, verbose_name='Texto de la Respuesta')
    clasificacion = models.ForeignKey(ClasificacionRespuesta, verbose_name='Clasificación de la Respuesta', on_delete=models.CASCADE, blank=True, null=True, default='')


class ApruebaJefe(models.Model):
    observacion_jefe = models.TextField(max_length=1000, default='', blank=True, verbose_name='Observaciones')
    fecha_jefe = models.DateTimeField(blank=True, default='', verbose_name= 'Fecha Aprobación Jefe', null=True)
    respuesta = models.ForeignKey(Respuesta, verbose_name='RespuestaJefe', on_delete=models.CASCADE, blank=True, null=True, default='')


class ApruebaDtr(models.Model):
    observacion_dtr = models.TextField(max_length=1000, default='', blank=True, verbose_name='Observaciones')
    fecha_dtr = models.DateTimeField(blank=True, default='', verbose_name= 'Fecha Aprobación Director', null=True)
    respuesta = models.ForeignKey(Respuesta, verbose_name='RespuestaDtr', on_delete=models.CASCADE, blank=True, null=True, default='')


class Tecnico (models.Model):
    profile = models.ForeignKey(Perfil, on_delete=False, related_name='profile')

    def __str__(self):
        return '{}'.format(self.profile.datos_personales.nombre + ' ' + self.profile.datos_personales.apellidos)



