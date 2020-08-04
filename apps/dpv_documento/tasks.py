from celery import shared_task
from celery.utils.log import get_task_logger
from locales_viv.celery import celery_app
from celery.schedules import crontab
import datetime

from .models import DPVDocumento


logger = get_task_logger(__name__)


@shared_task()
def check_day_on_document():
    for doc in DPVDocumento.objects.filter(dias__lt=180):
        if doc.fecha_registro.date() < datetime.datetime.now().date():
            tiempo = datetime.datetime.now().date() - doc.fecha_registro.date()
            doc.dias = tiempo.days
            doc.save()
    return True


celery_app.conf.beat_schedule = {
    'add-every-minute': {
        'task':  'apps.dpv_quejas.tasks.check_day_on_document',
        'schedule': crontab(minute='0', hour='6'),
    }
}