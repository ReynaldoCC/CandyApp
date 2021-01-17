from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger
from locales_viv.celery import celery_app
from celery.schedules import crontab
import datetime

from .models import Queja, TipoProcedencia


logger = get_task_logger(__name__)


@shared_task()
def check_date_on_quejas():
    for queja in Queja.objects.filter(notificada__isnull=True, rechazada__isnull=True):
        if queja.fecha_radicacion.date() < datetime.datetime.now().date():
            tiempo = datetime.datetime.now().date() - queja.fecha_radicacion.date()
            queja.tiempo = tiempo.days
            queja.save()
    return True


@shared_task()
def notify_queja(id_queja):
    queja = Queja.objects.filter(id=id_queja)
    if queja:
        queja = queja.first()
        anonimo = TipoProcedencia.objects.filter(nombre_icontains="anonimo").first()
        if queja.procedencia and queja.procedencia.tipo:
            if not queja.procedencia.tipo.enviar:
                return
            if queja.procedencia.tipo == anonimo:
                return
            email = queja.procedencia.objecto_contenido.get_email
            if not email:
                return
            send_mail("Ya esta la respuesta de la queja que nos ha entregado",
                      "Corre de aviso que tenemos la respuesta a su queja",
                      settings.EMAIL_FROM_USER,
                      [email, ])


celery_app.conf.beat_schedule = {
    'add-every-minute': {
        'task':  'apps.dpv_quejas.tasks.check_date_on_quejas',
        'schedule': crontab(minute='0', hour='6'),
    }
}
