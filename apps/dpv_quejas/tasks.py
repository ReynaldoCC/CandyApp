from celery import shared_task
from celery.utils.log import get_task_logger
from locales_viv.celery import celery_app
from celery.schedules import crontab
import datetime

from .models import Queja


logger = get_task_logger(__name__)


@shared_task()
def check_date_on_quejas():
    for queja in Queja.objects.filter(notificada__isnull=True, rechazada__isnull=True):
        if queja.fecha_radicacion.date() < datetime.datetime.now().date():
            tiempo = datetime.datetime.now().date() - queja.fecha_radicacion.date()
            queja.tiempo = tiempo.days
            queja.save()
    return True


celery_app.conf.beat_schedule = {
    'add-every-minute': {
        'task':  'apps.dpv_quejas.tasks.check_date_on_quejas',
        'schedule': crontab(minute='0', hour='6'),
    }
}
