from django.db import models

from .mixins import LoggerMixin


# Create your models here.
class FilesUploaded(LoggerMixin):
    nombre = models.CharField(max_length=255)
    tipo_mime = models.CharField(max_length=50)
    extencion = models.CharField(max_length=5)
    archivo = models.FileField()
    tamanno = models.DecimalField(max_digits=12, decimal_places=4)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre', 'extencion', ]

    def __str__(self):
        return '%s.%s' % (self.nombre, self.extencion)


class ConfigMail(LoggerMixin):
    servidor = models.CharField(max_length=100)
    puerto = models.CharField(max_length=3)
    usuario = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    usa_tls = models.BooleanField(default=False)
    usa_ssl = models.BooleanField(default=False)

    class Meta:
        verbose_name='Configuración de correo'

    def __str__(self):
        return self.servidor + ':' + self.puerto

