from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task()
def local_revision(local):
    local.get_ok_data()
    return True


@shared_task()
def list_local_revision(locales):
    for local in locales:
        local.get_ok_data()
