from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from apps.dpv_nomencladores.validators import *
from apps.dpv_nomencladores.models import Calle, Municipio, ConsejoPopular, TipoQueja, Procedencia, Estado,\
    CodificadorAsunto, AreaTrabajo, NivelSolucion, ConclusionCaso
from apps.dpv_respuesta.models import Respuesta, Tecnico, RespuestaAQueja
from apps.dpv_persona.models import PersonaNatural, PersonaJuridica
from apps.dpv_base.mixins import LoggerMixin


import uuid


def scramble_upload_document(instance, filename, subdiretory='quejas'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


class Damnificado(LoggerMixin):
    limit = models.Q(app_label='dpv_persona', model='personanatural') | \
        models.Q(app_label='dpv_persona', model='personajuridica')
    tipo_contenido = models.ForeignKey(ContentType, verbose_name=_('Damnificado de la queja'),
                                       limit_choices_to=limit,
                                       null=True, blank=True, on_delete=models.CASCADE)
    id_objecto = models.PositiveIntegerField(verbose_name=_('related object'), null=True)
    objecto_contenido = GenericForeignKey('tipo_contenido', 'id_objecto')

    class Meta:
        verbose_name = _("Damnificado")
        verbose_name_plural = _("Damnificados")

    def __str__(self):
        return "({}) {}".format(self.tipo_contenido, self.objecto_contenido)

    @property
    def get_tipo(self):
        return self.tipo_contenido.__str__()


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
    dir_cpopular = models.ForeignKey(ConsejoPopular, on_delete=models.CASCADE,
                                     verbose_name=_('Dirección Consejo Popular'))
    asunto = models.ForeignKey(CodificadorAsunto, verbose_name=_('Asunto Código'),
                               on_delete=models.CASCADE, blank=True, default='')
    asunto_texto = models.CharField(max_length=300, verbose_name=_("Asunto"), default='', blank=True)
    tipo = models.ForeignKey(TipoQueja, related_name="tipo_queja", on_delete=models.CASCADE,
                             blank=True, default='', verbose_name=_("Tipo"))
    numero = models.CharField(max_length=14, verbose_name=_('Número Queja'))
    codigo_numero = models.CharField(max_length=10, default='', blank=True)
    procedencia = models.ForeignKey(Procedencia, related_name="quejas",
                                    on_delete=models.CASCADE, blank=True, null=True, default='')
    no_procendencia = models.CharField(max_length=14, verbose_name=_("No. de Procedencia"), default='', blank=True)
    referencia = models.CharField(default='', max_length=50, blank=True, verbose_name='Referencia')
    estado = models.ForeignKey(Estado, verbose_name=_('Estado'),
                               on_delete=models.CASCADE, blank=True, default='')
    no_radicacion = models.CharField(verbose_name=_("No. Radicación Antiguo"), max_length=7, default='', blank=True)
    radicado_por = models.ForeignKey(User, on_delete=models.CASCADE,
                                     default='', blank='', verbose_name=_("Radicada Por"),
                                     related_name="quejas_radicadas")
    responder_a = models.ForeignKey(RespuestaAQueja, on_delete=models.CASCADE, verbose_name=_("Ofrecer respuesta a"),
                                    blank=True, null=True, default='')
    fecha_radicacion = models.DateTimeField(verbose_name=_("Fecha Radicación"), auto_now_add=True)
    fecha_termino = models.DateTimeField(verbose_name=_("Fecha Término"), auto_now_add=False, default=None, null=True)
    texto = models.TextField(max_length=3000, verbose_name='Cuerpo de la queja')
    tiempo = models.PositiveSmallIntegerField(verbose_name=_("Tiempo en proceso"), default=0,
                                              help_text=_("Tiempo en días que tiene de radicada la queja"))
    document = models.FileField(verbose_name=_("Copia digital"), upload_to=scramble_upload_document,
                                null=True, blank=True, default=None)
    damnificado = models.ForeignKey(Damnificado, on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)

    class Meta:
        verbose_name = _("Queja")
        verbose_name_plural = _("Quejas")

    def __str__(self):
        return self.numero

    @property
    def get_quejoso(self):
        return self.damnificado

    @property
    def get_tecnico_asignado(self):
        if self.quejatecnico.filter(rechazada__isnull=True).exists():
            return self.quejatecnico.filter(rechazada__isnull=True).first().tecnico
        else:
            return None

    @property
    def get_respuesta(self):
        return self.respuesta.filter(rechazada__isnull=True).first()


class AsignaQuejaDpto(LoggerMixin):
    asignador = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    quejadpto = models.ForeignKey(Queja, related_name='quejadpto', on_delete=models.CASCADE,
                                  blank=True, null=True, default='')
    dpto = models.ForeignKey(AreaTrabajo, related_name='dpto', on_delete=models.CASCADE,
                             blank=True, null=True, default='')
    observaciones = models.TextField(verbose_name=_("Observaciones"), blank=True, default='')
    fecha_asignacion = models.DateTimeField(verbose_name=_("Fecha Asignación"), auto_now_add=True)
    rechazada = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        verbose_name = _("Queja asignada a Depto")
        verbose_name_plural = _("Quejas asignadas a Depto")


class AsignaQuejaTecnico(LoggerMixin):
    asignador = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    quejatecnico = models.ForeignKey(Queja, related_name='quejatecnico', on_delete=models.CASCADE,
                                     blank=True, null=True, default='')
    tecnico = models.ForeignKey(Tecnico, related_name='tecnico', on_delete=models.CASCADE,
                                blank=True, null=True, default='')
    observaciones = models.TextField(verbose_name=_("Observaciones"), blank=True, default='')
    fecha_asignacion = models.DateTimeField(verbose_name=_("Fecha Asignación"), auto_now_add=True)
    rechazada = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        verbose_name = _("Queja asignada a Técnico")
        verbose_name_plural = _("Quejas asignadas a Técnico")


class QuejaRechazada(LoggerMixin):
    queja = models.ForeignKey(Queja, related_name='rechazada', on_delete=models.CASCADE,
                              blank=True, null=True, default='')
    motivo = models.TextField(verbose_name=_("Motivo de Rechazo"),
                              help_text=_("Motivo por el cual se rechaza la queja"),
                              default='Motivo por defecto')
    rechazada_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Rechazada Por"),
                                      blank=True, default='')

    class Meta:
        verbose_name = _("Queja Rechazada")
        verbose_name_plural = _("Quejas Rechazadas")


class QuejaRedirigida(LoggerMixin):
    queja = models.ForeignKey(Queja, related_name='redirigida', on_delete=models.CASCADE,
                              blank=True, null=True, default='')
    motivo = models.TextField(verbose_name=_("Motivo de Rechazo"),
                              help_text=_("Motivo por el cual se rechaza la queja"),
                              default='Motivo por defecto')
    redirigida_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Rechazada Por"),
                                       blank=True, default='')


class RespuestaQueja(Respuesta):
    queja = models.ForeignKey(Queja, related_name='respuesta', on_delete=models.CASCADE,
                              blank=True, null=True, default='')
    gestion = models.TextField(verbose_name=_("Gestion realizada"),
                               blank=True,
                               default="",
                               help_text=_("Gestion realizada por parte del tecnico para dar respuesta a la queja"))
    nivel_solucion = models.ForeignKey(NivelSolucion, verbose_name=_("Nivel de la Solución"), on_delete=models.CASCADE,
                                       default=None, null=True)
    conclusion_caso = models.ForeignKey(ConclusionCaso, verbose_name=_("Conclusión del Caso"), on_delete=models.CASCADE,
                                        default=None, null=True)

    class Meta:
        verbose_name = _("Respuesta a Queja")
        verbose_name_plural = _("Respuestas a Quejas")

    def __str__(self):
        return self.codigo


class QuejaNotificada(LoggerMixin):
    queja = models.ForeignKey(Queja, related_name='notificada', on_delete=models.CASCADE,
                              blank=True, null=True, default='')
    notificada = models.DateTimeField(default=None, null=True, verbose_name=_("Notificada"))
    notificador = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Quien notifica."),
                                    default='', blank=True)
