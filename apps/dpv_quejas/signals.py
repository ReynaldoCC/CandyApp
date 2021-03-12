from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.dpv_nomencladores.models import AreaTrabajo, Estado
from apps.dpv_notificaciones.tasks import make_notification

from .models import Queja, AsignaQuejaDpto, AsignaQuejaTecnico, QuejaNotificada, QuejaRedirigida, RespuestaQueja

import datetime


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
                except ValueError:
                    consecutivo = '0001'
            else:
                try:
                    consecutivo = str(int(ultima_queja.numero[10:])+1).zfill(4)
                except:
                    consecutivo = '0001'
                # revisar a partir de que parte del codigo falla
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

    if radicada and not asig_depto and not asig_tec and not resp and not apr and not apr_dtr and not deny_resp \
            and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=1).first()
    elif radicada and deny and redir and not noti:
        instance.estado = Estado.objects.filter(id=8).first()
    elif radicada and deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=9).first()
    elif radicada and asig_depto and not asig_tec and not resp and not apr and not apr_dtr and not deny_resp \
            and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=2).first()
    elif radicada and asig_depto and asig_tec and not resp and not apr and not apr_dtr and not deny_resp \
            and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=3).first()
    elif radicada and asig_depto and asig_tec and not resp and not apr and not apr_dtr and deny_resp \
            and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=10).first()
    elif radicada and asig_depto and asig_tec and resp and not apr and not apr_dtr and not deny_resp \
            and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=4).first()
    elif radicada and asig_depto and asig_tec and resp and apr and not apr_dtr and not deny_resp \
            and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=5).first()
    elif radicada and asig_depto and asig_tec and resp and apr and apr_dtr and not deny_resp \
            and not deny and not redir and not noti:
        instance.estado = Estado.objects.filter(id=6).first()
    elif radicada and asig_depto and asig_tec and resp and apr and apr_dtr and not deny_resp \
            and not deny and not redir and noti:
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
        data = {
            'user_id': instance.tecnico.id,
            'text': _('Le ha sido asignada la queja no. ' + instance.quejatecnico.numero +
                      ' por el usuario ' + instance.asignador.get_full_name()),
            'level': 1,
        }
        make_notification.delay(data)


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
