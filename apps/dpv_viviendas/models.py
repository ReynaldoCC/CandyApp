from django.db import models
from apps.dpv_nomencladores.models import Destino, Concepto
from apps.dpv_persona.models import PersonaNatural
from apps.dpv_locales.models import Local
from apps.dpv_base.mixins import LoggerMixin


# Create your models here.
class Vivienda(LoggerMixin):
    numero = models.PositiveSmallIntegerField()
    destino = models.ForeignKey(Destino, help_text="Destino para la vivienda", related_name="locales_dest", on_delete=models.CASCADE)
    cantidad_persona = models.PositiveSmallIntegerField(help_text="Cantidad de personas que viven en la vivienda")
    cantidad_menores = models.PositiveSmallIntegerField(help_text="Cantidad de menores de edad que conviven en la vivienda", default=0, verbose_name='Cantidad de Menores de Edad', blank=True)
    cantidad_mujeres = models.PositiveSmallIntegerField(help_text="Cantidad de mujeres que conviven en la vivienda", default=0, verbose_name='Cantidad de Mujeres', blank=True)
    cantidad_aclifim = models.PositiveSmallIntegerField(help_text="Cantidad de impedidos físicos que conviven en la vivienda", default=0, verbose_name='Cantidad de Impedidos Físicos', blank=True)
    cantidad_anciano = models.PositiveSmallIntegerField(help_text="Cantidad de personas de la 3ra edad que conviven en la vivienda", default=0, verbose_name='Cantidad de Personas de 3ra Edad', blank=True)
    propietario = models.ForeignKey(PersonaNatural, related_name="vivienada_prop", on_delete=models.CASCADE)
    fecha_propietario = models.DateField(verbose_name="Fecha de habitado", auto_now=False, auto_now_add=False)
    concepto = models.ForeignKey(Concepto, verbose_name="Concepto", help_text="Concepto de uso de la vivienda", on_delete=models.CASCADE)
    aprobada = models.BooleanField(default=False, verbose_name="Aprobación dada", help_text="Marcar si la vivienda esta aprobada.")
    add_concepto = models.CharField(max_length=500, verbose_name="Datos Concepto", blank=True)
    local_dado = models.ForeignKey(Local, related_name="vivienda_local", help_text="Local donde se encuentra la vivienda.", on_delete=models.CASCADE, default='')

    class Meta:
        verbose_name = "Vivienda"
        verbose_name_plural = "Viviendas"
        ordering = ['numero']
        unique_together = ('numero', 'local_dado', )

    def __str__(self):
        return str(self.numero)
