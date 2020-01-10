from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from apps.dpv_nomencladores.validators import *
from apps.dpv_nomencladores.models import *
from apps.dpv_respuesta.models import *
from apps.dpv_persona.models import *
from django.utils import timezone

class Queja(models.Model):
    person_natural = models.ForeignKey(PersonaNatural, related_name='person_natural', on_delete=False,
                                       blank=True, null=True, default='')
    empresa = models.ForeignKey(PersonaJuridica, related_name='person_juridic', on_delete=models.CASCADE,blank=True, null=True,
                                default='')
    dir_num = models.CharField(max_length=15, verbose_name='dir_numero')
    dir_calle = models.ForeignKey(Calle, verbose_name='dir_calle', on_delete=models.CASCADE, blank=True, null=True, default='')
    dir_entrecalle1 = models.ForeignKey(Calle, verbose_name='dir_entrecalle1', on_delete=models.CASCADE, blank=True, null=True,
                                  default='')
    dir_entrecalle2 = models.ForeignKey(Calle, verbose_name='dir_entrecalle2', on_delete=models.CASCADE, blank=True, null=True,
                                  default='')
    asunto = models.ForeignKey(CodificadorAsunto, verbose_name='asunto_queja', on_delete=models.CASCADE, blank=True, null=True,
                                        default='')
    numero = models.CharField(max_length=10, verbose_name='numero')
    procedencia = models.ForeignKey(Procedencia, related_name="prodencia", on_delete=False,blank=True, null=True, default='')
    referencia = models.CharField(default='', max_length=50, blank=True, verbose_name='Referencia')
    estado = models.ForeignKey(Estado, verbose_name='estado', on_delete=models.CASCADE, blank=True, null=True, default='')
    fecha_ultima_accion = models.DateTimeField(default=timezone.now)
    texto = models.TextField(max_length=1000, verbose_name='Cuerpo de la queja')
    respuesta = models.ForeignKey(Respuesta, verbose_name='respuesta_queja', on_delete=models.CASCADE, blank=True, null=True, default='')
    clasificacion = models.ForeignKey(TipoQueja, verbose_name='Tipo de Queja', on_delete=models.CASCADE, blank=True, null=True, default='')


class AsignaQuejaDpto(models.Model):
    quejadpto = models.ForeignKey(Queja, related_name='quejadpto', on_delete=False, blank=True, null=True, default='')
    dpto = models.ForeignKey(AreaTrabajo, related_name='dpto', on_delete=False, blank=True, null=True, default='')


class AsignaQuejaTecnico(models.Model):
    quejatecnico = models.ForeignKey(Queja, related_name='quejatecnico', on_delete=False, blank=True, null=True, default='')
    tecnico = models.ForeignKey(Tecnico, related_name='tecnico', on_delete=False, blank=True, null=True, default='')




