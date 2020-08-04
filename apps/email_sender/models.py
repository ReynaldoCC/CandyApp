from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from django.core.mail import EmailMessage
from apps.dpv_base.mixins import LoggerMixin
from .validators import validate_ip46_fqdn_address


# Create your models here.

class EmailConfigurate(LoggerMixin):
    puerto = models.PositiveSmallIntegerField(verbose_name='Puerto', blank=True, null=True, validators=[MinValueValidator(1)], help_text="Puerto de conección al servidor.")
    servidor = models.CharField(max_length=255, verbose_name='Servidor', help_text="Servidor SMTP por donde se enviarán los correos.", blank=True , validators=[MinLengthValidator(8), MaxLengthValidator(255), validate_ip46_fqdn_address])
    use_tls = models.BooleanField(default=False, verbose_name='Seguridad con TLS', help_text="Marque si el servidor usa seguridad TLS")
    use_ssl = models.BooleanField(default=False, verbose_name='Seguridad con SSL', help_text="Marque si el servidor usa seguridad SSL")
    usuario = models.CharField(max_length=255, blank=True, verbose_name="Usuario", help_text="Usuario para autenticarse en el servidor", validators=[MinLengthValidator(4), MaxLengthValidator(255)])
    password = models.CharField(max_length=50, blank=True, verbose_name='Contraseña', help_text="Contraseña del usuario para authenticarse en el servidor.", validators=[MinLengthValidator(8), MaxLengthValidator(50)])

    class Meta:
        ordering = ["servidor", ]
        verbose_name = "COnfiguración de Correo"
        verbose_name_plural = "Configuraciones de Correo"