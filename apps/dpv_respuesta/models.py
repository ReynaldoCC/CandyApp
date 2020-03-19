from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.dpv_nomencladores.models import *
from apps.dpv_perfil.models import *
from apps.dpv_base.mixins import LoggerMixin


class Tecnico (LoggerMixin):
    profile = models.ForeignKey(Perfil, on_delete=False, related_name='profile')

    def __str__(self):
        return '{}'.format(self.profile.datos_personales.nombre + ' ' + self.profile.datos_personales.apellidos)



class Respuesta(LoggerMixin):
    fecha_respuesta = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de Respuesta"))
    rechazada = models.DateTimeField(default=None, null=True)
    codigo = models.CharField(verbose_name=_("Código de la Respuesta"), max_length=14)
    texto = models.TextField(max_length=1000, default='', blank=True, verbose_name='Texto de la Respuesta')
    responde = models.ForeignKey(Tecnico, on_delete=models.CASCADE, default='', blank=True)
    clasificacion = models.ForeignKey(ClasificacionRespuesta, verbose_name='Clasificación de la Respuesta', on_delete=models.CASCADE, blank=True, null=True, default='')

    class Meta:
        verbose_name = _("Respuesta")
        verbose_name_plural = _("RespuestaS")


class ApruebaJefe(LoggerMixin):
    observacion_jefe = models.TextField(max_length=1000, default='', blank=True, verbose_name=_('Observaciones'))
    fecha_jefe = models.DateTimeField(blank=True, default='', verbose_name=_('Fecha Aprobación Jefe'), null=True)
    respuesta = models.ForeignKey(Respuesta, verbose_name=_('Respuesta Dada'), on_delete=models.CASCADE, blank=True, null=True, default='')
    aprobada_por = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Respuesta Aprobada por Jefe")
        verbose_name_plural = _("Respuestas Aprobadas por Jefe")


class ApruebaDtr(LoggerMixin):
    observacion_dtr = models.TextField(max_length=1000, default='', blank=True, verbose_name=_('Observaciones'))
    fecha_dtr = models.DateTimeField(blank=True, default='', verbose_name=_('Fecha Aprobación Director'), null=True)
    respuesta = models.ForeignKey(Respuesta, verbose_name=_('Respuesta Dada'), on_delete=models.CASCADE, blank=True, null=True, default='')
    aprobada_por = models.ForeignKey(Perfil, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Respuesta Aprobada por Director")
        verbose_name_plural = _("Respuestas Aprobadas por Director")


class RespuestaRechazada(LoggerMixin):
    NIVEL_CHOICES = (
        (1, 'Jefe de Departamento'),
        (2, 'Director'),
    )
    fecha_rechazada = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha del Rechazo"))
    argumento = models.TextField(verbose_name=_("Argumento"), default=_("Argumento de rechazo por defecto"))
    rechazador = models.ForeignKey(User, on_delete=models.CASCADE,
                                   verbose_name=_("Quien Rechaza"), default='', blank=True)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, default='', blank=True)
    nivel = models.PositiveSmallIntegerField(default=0, choices=NIVEL_CHOICES)




