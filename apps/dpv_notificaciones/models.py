from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.utils import timesince

from apps.dpv_base.mixins import LoggerMixin

User = get_user_model()


# Create your models here.
class Notify(LoggerMixin):
    """
    Model for save and works with notifications, notifications are system messages about events and actions
    """
    main_text = models.TextField(verbose_name=_("Texto"), default="", blank=True, null=True)
    user = models.ForeignKey(User, verbose_name=_("Usuario notificado"),
                             on_delete=models.CASCADE, default=None, blank=True, null=True)
    date_time = models.DateTimeField(verbose_name=_("Fecha de la notificación"), auto_now_add=True, null=True)
    level = models.PositiveSmallIntegerField(verbose_name=_(""), default=0, blank=True, null=True)
    readed = models.BooleanField(verbose_name=_("Visto"), default=False)

    class Meta:
        verbose_name = _("Notificación")
        verbose_name_plural = _("Notificaciones")
        ordering = ("-date_time", "user")

    def __str__(self):
        """
        Redefine the way if showed notify object
        :return: String with the date of notification and 55 characters of notification text
        """
        return "{}: {}".format(timesince.timesince(self.date_time), self.main_text[:55] + "...")
