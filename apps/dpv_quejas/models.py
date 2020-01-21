from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.dpv_nomencladores.validators import *
from apps.dpv_nomencladores.models import *
from apps.dpv_respuesta.models import *
from apps.dpv_persona.models import *
from apps.dpv_base.mixins import LoggerMixin
from django.utils import timezone


class Queja(LoggerMixin):
    dir_num = models.CharField(max_length=15, verbose_name=_('Dirección Número'))
    dir_calle = models.ForeignKey(Calle, verbose_name=_('Dirección Calle'), related_name='queja_calle',
                                  on_delete=models.CASCADE, blank=True, default='')
    dir_entrecalle1 = models.ForeignKey(Calle, verbose_name=_('Dirección Primera Entrecalle'),
                                        on_delete=models.CASCADE, blank=True, default='',
                                        related_name='queja_entrecalle1')
    dir_entrecalle2 = models.ForeignKey(Calle, verbose_name=_('Dirección Segunda Entrecalle'),
                                        on_delete=models.CASCADE, blank=True, default='',
                                        related_name='queja_entrecalle2')
    dir_municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name=_('Dirección Municipio'))
    dir_cpopular = models.ForeignKey(ConsejoPopular, on_delete=models.CASCADE, verbose_name=_('Dirección Consejo Popular'))
    asunto = models.ForeignKey(CodificadorAsunto, verbose_name=_('Asunto Queja'),
                               on_delete=models.CASCADE, blank=True, default='')
    numero = models.CharField(max_length=10, verbose_name=_('Número Queja'))
    procedencia = models.ForeignKey(Procedencia, related_name="prodencia",
                                    on_delete=models.CASCADE, blank=True, null=True, default='')
    referencia = models.CharField(default='', max_length=50, blank=True, verbose_name='Referencia')
    estado = models.ForeignKey(Estado, verbose_name=_('Estado'),
                               on_delete=models.CASCADE, blank=True, default='')
    fecha_radicacion = models.DateTimeField(verbose_name=_("Fecha Radicación"), auto_now_add=True)
    texto = models.TextField(max_length=3000, verbose_name='Cuerpo de la queja')
    tiempo = models.PositiveSmallIntegerField(verbose_name=_("Tiempo en proceso"), default=0,
                                              help_text=_("Tiempo en días que tiene de radicada la queja"))
    clasificacion = models.ForeignKey(TipoQueja, verbose_name='Tipo de Queja',
                                      on_delete=models.CASCADE, blank=True, default='')

    class Meta:
        verbose_name = _("Queja")
        verbose_name_plural = _("Quejas")


class Damnificado(LoggerMixin):
    queja = models.ForeignKey(Queja, on_delete=models.CASCADE, related_name='damnificado')

    class Meta:
        verbose_name = _("Damnificado")
        verbose_name_plural = _("Damnificados")


class DamnificadoNatural(Damnificado):
    persona_natural = models.ForeignKey(PersonaNatural, related_name='persona_natural', on_delete=models.CASCADE,
                                        blank=True, null=True, default='')


class DamnificadoJuridico(Damnificado):
    persona_juridica = models.ForeignKey(PersonaJuridica, related_name='persona_juridica', on_delete=models.CASCADE,
                                         blank=True, null=True, default='')


class AsignaQuejaDpto(LoggerMixin):
    quejadpto = models.ForeignKey(Queja, related_name='quejadpto', on_delete=models.CASCADE, blank=True, null=True, default='')
    dpto = models.ForeignKey(AreaTrabajo, related_name='dpto', on_delete=models.CASCADE, blank=True, null=True, default='')
    observaciones = models.TextField(verbose_name=_("Observaciones"), blank=True, default='')
    fecha_asignacion = models.DateTimeField(verbose_name=_("Fecha Asignación"), auto_now_add=True)
    rechazada = models.DateTimeField(default=None, null=True)

    class Meta:
        verbose_name = _("Queja asignada a Depto")
        verbose_name_plural = _("Quejas asignadas a Depto")


class AsignaQuejaTecnico(LoggerMixin):
    quejatecnico = models.ForeignKey(Queja, related_name='quejatecnico', on_delete=models.CASCADE, blank=True, null=True, default='')
    tecnico = models.ForeignKey(Tecnico, related_name='tecnico', on_delete=models.CASCADE, blank=True, null=True, default='')
    observaciones = models.TextField(verbose_name=_("Observaciones"), blank=True, default='')
    fecha_asignacion = models.DateTimeField(verbose_name=_("Fecha Asignación"), auto_now_add=True)
    rechazada = models.DateTimeField(default=None, null=True)

    class Meta:
        verbose_name = _("Queja asignada a Técnico")
        verbose_name_plural = _("Quejas asignadas a Técnico")


class QuejaRechazada(LoggerMixin):
    queja = models.ForeignKey(Queja, related_name='rechazada', on_delete=models.CASCADE, blank=True, null=True, default='')
    motivo = models.TextField(verbose_name=_("Motivo de Rechazo"),
                              help_text=_("Motivo por el cual se rechaza la queja"),
                              default='Motivo por defecto')
    rechazada_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Rechazada Por"), blank=True, default='')

    class Meta:
        verbose_name = _("Queja Rechazada")
        verbose_name_plural = _("Quejas Rechazadas")


class QuejaRedirigida(LoggerMixin):
    queja = models.ForeignKey(Queja, related_name='redirigida', on_delete=models.CASCADE, blank=True, null=True, default='')
    motivo = models.TextField(verbose_name=_("Motivo de Rechazo"),
                              help_text=_("Motivo por el cual se rechaza la queja"),
                              default='Motivo por defecto')
    redirigida_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Rechazada Por"), blank=True, default='')


class RespuestaQueja(Respuesta):
    queja = models.ForeignKey(Queja, related_name='respuesta', on_delete=models.CASCADE, blank=True, null=True, default='')


class QuejaNotificada(LoggerMixin):
    queja = models.ForeignKey(Queja, related_name='notificada', on_delete=models.CASCADE, blank=True, null=True, default='')
    notificada = models.DateTimeField(default=None, null=True, verbose_name=_("Notificada"))
    notificador = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Quien notifica."), default='', blank=True)


# Utils functionalities
def configurar_numero_queja(instancia=None, sender=None):
    if instancia and instancia.id:
        ultima_queja = sender.objects.exclude(id=instancia.id).filter(fecha_radicacion__year=timezone.now().year).order_by('numero').last()
    else:
        ultima_queja = sender.objects.filter(fecha_radicacion__year=timezone.now().year).order_by('numero').last()
    if ultima_queja:
        ultimo_numero = ultima_queja.numero
        if len(ultimo_numero) < 14:
            if len(ultimo_numero) >= 10:
                consecutivo = str(int(ultimo_numero[10:])+1).zfill(4)
            else:
                ultima_queja.save()
                consecutivo = str(int(ultima_queja.numero[10:])+1).zfill(4)
                # revisar a partir de que pardete del codigo falla
        elif len(ultimo_numero) < 14:
            consecutivo = str(int(ultimo_numero[10:])+1).zfill(4)
        else:
            consecutivo = str(int(ultimo_numero[-4:])+1).zfill(4)

        instancia.numero = '{%s%s%s%s%s%s}' % (instancia.dir_municipio.provincia.numero,
                                            instancia.dir_municipio.numero,
                                            instancia.dir_cpopular,
                                            timezone.now().strftime('%y'),
                                            timezone.now().strftime('%m'),
                                            consecutivo)


def configurar_estado(instance):
    if not instance or instance is None:
        return


# Signals
@receiver(pre_save, sender=Queja)
def preset_queja(sender, **kwargs):
    if kwargs.get('instance'):
        instance = kwargs.get('instance')
        if instance.numero == '' or not instance.numero:
            configurar_numero_queja(instance, sender)
        configurar_estado(instance)
