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
import datetime


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
    tipo = models.ForeignKey(TipoQueja, related_name="tipo_queja", on_delete=models.CASCADE, blank=True, default='', verbose_name=_("Tipo"))
    numero = models.CharField(max_length=14, verbose_name=_('Número Queja'))
    codigo_numero = models.CharField(max_length=10, default='', blank=True)
    procedencia = models.ForeignKey(Procedencia, related_name="prodencia",
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

    class Meta:
        verbose_name = _("Queja")
        verbose_name_plural = _("Quejas")

    def __str__(self):
        return self.numero

    @property
    def get_quejoso(self):
        return self.damnificado.first().objecto_contenido

    @property
    def get_tecnico_asignado(self):
        if self.quejatecnico.filter(rechazada__isnull=True).exists():
            return self.quejatecnico.filter(rechazada__isnull=True).first().tecnico
        else:
            return None


class Damnificado(LoggerMixin):
    queja = models.ForeignKey(Queja, on_delete=models.CASCADE, related_name='damnificado')
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


class AsignaQuejaDpto(LoggerMixin):
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


# Utils functionalities
def configurar_numero_queja(instancia=None, sender=None):
    if instancia and instancia.id:
        ultima_queja = sender.objects.exclude(id=instancia.id)\
            .filter(fecha_radicacion__year=timezone.now().year).order_by('numero').last()
    else:
        ultima_queja = sender.objects.filter(fecha_radicacion__year=timezone.now().year).order_by('numero').last()
    if ultima_queja:
        ultimo_numero = ultima_queja.numero
        if len(ultimo_numero) < 14:
            if len(ultimo_numero) >= 10:
                try:
                    consecutivo = str(int(ultimo_numero[10:])+1).zfill(4)
                except:
                    consecutivo = '0001'
            else:
                try:
                    consecutivo = str(int(ultima_queja.numero[10:])+1).zfill(4)
                except:
                    consecutivo = '0001'
                # revisar a partir de que pardete del codigo falla
        elif len(ultimo_numero) < 14:
            consecutivo = str(int(ultimo_numero[10:])+1).zfill(4)
        else:
            consecutivo = str(int(ultimo_numero[-4:])+1).zfill(4)

        instancia.numero = '%s%s%s%s%s%s' % (str(instancia.dir_municipio.provincia.numero).zfill(2),
                                             str(instancia.dir_municipio.numero).zfill(2),
                                             str(instancia.dir_cpopular.numero).zfill(2),
                                             timezone.now().strftime('%y'),
                                             timezone.now().strftime('%m'),
                                             consecutivo)
    else:
        instancia.numero = '%s%s%s%s%s%s' % (str(instancia.dir_municipio.provincia.numero).zfill(2),
                                             str(instancia.dir_municipio.numero).zfill(2),
                                             str(instancia.dir_cpopular.numero).zfill(2),
                                             timezone.now().strftime('%y'),
                                             timezone.now().strftime('%m'),
                                             '0001')


def configurar_estado(instance):
    """
    Este método le asigna un estado a la queja que recibe como instancia que segun los
    relaciones con su respuesta, asignacion, rechazo, redirección

    :param instance:
    :return:
    """
    if not instance or instance is None:
        return
    radicada = True
    asig_depto = False
    asig_tec = False
    resp = False
    deny_resp = False
    apr = False
    apr_dtr = False
    noti = False
    redir = False
    deny = False

    if instance.quejadpto.exists():
        asig_depto = True
    if instance.quejatecnico.exists():
        asig_tec = True
    if instance.respuesta.filter(rechazada__isnull=True).exists():
        resp = True
        if instance.respuesta.filter(rechazada__isnull=True).first().apruebajefe_set.exists():
            apr = True
        if instance.respuesta.filter(rechazada__isnull=True).first().apruebadtr_set.exists():
            apr_dtr = True
    if instance.respuesta.count() == instance.respuesta.filter(rechazada__isnull=False).count():
        if instance.respuesta.count() > 0:
            deny_resp = True
    if instance.rechazada.exists():
        deny = True
    if instance.redirigida.exists():
        redir = True
    if instance.notificada.exists():
        noti = True

    if radicada and not asig_depto and not asig_tec and not resp and not apr and not apr_dtr and not deny_resp and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=1).first()
    elif radicada and deny and redir and not noti:
        instance.estado = Estado.objects.filter(id=8).first()
    elif radicada and deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=9).first()
    elif radicada and asig_depto and not asig_tec and not resp and not apr and not apr_dtr and not deny_resp and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=2).first()
    elif radicada and asig_depto and asig_tec and not resp and not apr and not apr_dtr and not deny_resp and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=3).first()
    elif radicada and asig_depto and asig_tec and not resp and not apr and not apr_dtr and deny_resp and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=10).first()
    elif radicada and asig_depto and asig_tec and resp and not apr and not apr_dtr and not deny_resp and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=4).first()
    elif radicada and asig_depto and asig_tec and resp and apr and not apr_dtr and not deny_resp and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=5).first()
    elif radicada and asig_depto and asig_tec and resp and apr and apr_dtr and not deny_resp and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=6).first()
    elif radicada and asig_depto and asig_tec and resp and apr and apr_dtr and not deny_resp and not deny and not redir and noti:
        instance.estado = Estado.objects.filter(id=7).first()
    else:
        instance.estado = Estado.objects.filter(id=11).first()


def configurar_fecha_termino(instance):
    if not instance or instance is None:
        return
    try:
        if not instance.fecha_termino or instance.fecha_termino is None:
            if not instance.fecha_radicacion or instance.fecha_radicacion is None:
                today = timezone.now()
            else:
                today = instance.fecha_radicacion
            if not instance.procedencia or instance.procedencia is None:
                time_response = 30
            else:
                time_response = instance.procedencia.tipo.cant_dias
            instance.fecha_termino = today + datetime.timedelta(days=time_response)
    except ValueError as e:
        print(str(e))


def configurar_codigo_numero(instance):
    if not instance or instance is None:
        return
    try:
        if not instance.codigo_numero and instance.tipo and instance.asunto:
            instance.codigo_numero = "{}-{}".format(instance.tipo.numero, instance.asunto.numero)
    except ValueError as e:
        print(e)


def asignar_depto_ap(instance):
    """
    Este metodo hecho para ser llamado en el signal pre-save y lo que hace es a a la instancia de queja
    que recibe por parametro la asigna por defecto al depto. de atención a la población para su procesamiento.
    :param instance:
    :return:
    """
    if not instance or instance is None:
        return
    if not instance.quejadpto.exists():
        qd = AsignaQuejaDpto()
        qd.quejadpto = instance
        qd.dpto = AreaTrabajo.objects.filter(nombre__icontains='atenci').filter(nombre__icontains='poblaci').first()
        qd.observaciones = "Asignado por el sistema."
        qd.save()


# Signals
@receiver(pre_save, sender=Queja)
def preset_queja(sender, **kwargs):
    if kwargs.get('instance'):
        instance = kwargs.get('instance')
        if kwargs.get('created', True):
            if instance.numero == '' or not instance.numero:
                configurar_numero_queja(instance, sender)
            configurar_fecha_termino(instance)
            configurar_codigo_numero(instance)
        configurar_estado(instance)


@receiver(post_save, sender=Queja)
def postset_queja(sender, **kwargs):
    if kwargs.get('instance'):
        instance = kwargs.get('instance')
        if kwargs.get('created', True):
            asignar_depto_ap(instance)


@receiver(post_save, sender=AsignaQuejaTecnico)
def set_queja_asigtec_state(sender, **kwargs):
    if kwargs.get('instance'):
        instance = kwargs.get('instance')
        instance.quejatecnico.save()


@receiver(post_save, sender=AsignaQuejaDpto)
def set_queja_asigdpto_state(sender, **kwargs):
    if kwargs.get('instance'):
        instance = kwargs.get('instance')
        instance.quejadpto.save()


@receiver(post_save, sender=QuejaNotificada)
def set_queja_noti_state(sender, **kwargs):
    if kwargs.get('instance'):
        instance = kwargs.get('instance')
        instance.queja.save()


# @receiver(post_save, sender=RespuestaAQueja)
# def set_queja_resp_state(sender, **kwargs):
#     if kwargs.get('instance'):
#         instance = kwargs.get('instance')
#         instance.queja.save()


@receiver(post_save, sender=QuejaRedirigida)
def set_queja_redir_state(sender, **kwargs):
    if kwargs.get('instance'):
        instance = kwargs.get('instance')
        instance.queja.save()


@receiver(pre_save, sender=RespuestaQueja)
def preset_respuesta(sender, **kwargs):
    if kwargs.get('instance'):
        instance = kwargs.get('instance')
        if instance.queja and not instance.codigo:
            counter = instance.queja.respuesta.count() + 1
            instance.codigo = instance.queja.numero + str(counter)

