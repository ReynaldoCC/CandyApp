from celery import shared_task
from celery.utils.log import get_task_logger

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.defaulttags import url
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .models import Notify

logger = get_task_logger(__name__)


@shared_task()
def make_notification(data):
    """
    This function make a notify to user for that propouse receive data param that is a dictionary with the keys
    user_id: Int pk of user to make the notify
    text: String for the body of notify
    level: Int to represent the level of importance of notify
    :param data: Python dictionary
    :return: None
    """
    if not data or data is None:
        return
    user = User.objects.filter(pk=data["user_id"])
    if not user or user is None:
        return
    n = Notify()
    n.user = user.first()
    n.level = data["level"] or 0
    n.main_text = data["text"]
    n.save()
    """
    If the user of the notify have activated the flag to receive email when have a new notify, then try send and email
    """
    if user.perfil_usuario.notificacion_email:
        message_body = """
        Te ha llegado una nueva notificación que se ha generado debido ha algún evento del sistema que te involucra,
        puedes ver todas las notificaciones desde este enlace 
        """ + url("notifies")
        send_mail(_("Tienes una nueva notificación"),
                  _(message_body),
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email],
                  fail_silently=False)
