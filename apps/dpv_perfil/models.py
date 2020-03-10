from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.dpv_persona.models import PersonaNatural
from apps.dpv_nomencladores.models import AreaTrabajo, CentroTrabajo, Genero, Calle, ConsejoPopular, Municipio
from apps.dpv_base.mixins import LoggerMixin
from random import randint
import uuid
import datetime


# Create your models here.
def scramble_upload_avatar(instance, filename, subdiretory='avatars'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


class Perfil(LoggerMixin):
    datos_usuario = models.OneToOneField(User, verbose_name="Datos del usuario", related_name="perfil_usuario", on_delete=models.CASCADE)
    datos_personales = models.OneToOneField(PersonaNatural, verbose_name="Datos Personales", related_name="perfil_datos", on_delete=models.CASCADE)
    notificacion_email = models.BooleanField(default=True, verbose_name="Notificar por Email",
                                             help_text="Marque para recibir las notificaciones por correo electrónico")
    documentacion_email = models.BooleanField(default=True, verbose_name="Recibir Documentos por Email",
                                              help_text="Marque para recibir la documentación por correo electronico")
    avatar = models.ImageField('avatars', upload_to=scramble_upload_avatar, blank=True, null=True)
    centro_trabajo = models.ForeignKey(CentroTrabajo, verbose_name="Unidad", related_name="perfil_trabajo", on_delete=models.SET_DEFAULT, default='')
    depto_trabajo = models.ForeignKey(AreaTrabajo, verbose_name="Departamento", related_name="perfil_area", on_delete=models.SET_DEFAULT, default='')

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"


 # Signals
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, **kwargs):
    if kwargs.get('created', False):
        print('usuario creado', kwargs)
        if kwargs.get('instance'):
            instance = kwargs.get('instance')
            if instance.is_superuser:
                p = Perfil()
                p.centro_trabajo = CentroTrabajo.objects.filter(oc=True).first()
                p.depto_trabajo = AreaTrabajo.objects.all().first()
                numero = str(randint(10000, 99999))
                date = datetime.date.today().strftime('%y%m%d')
                per = PersonaNatural()
                per.nombre = "Desarrollador"
                per.apellidos = "Implatación y Despliegue"
                per.ci = "{}{}".format(date, numero)
                per.genero = Genero.objects.first()
                per.email_address = instance.email or "{}{}@email.cu".format(instance.username, str(randint(50, 90)))
                per.direccion_numero = str(randint(1, 4000))
                per.direccion_calle = Calle.objects.first()
                per.direccion_entrecalle1 = Calle.objects.last()
                per.direccion_entrecalle2 = Calle.objects.filter(id__in=[3, 4, 5, 6]).last()
                per.municipio = Municipio.objects.first()
                per.cpopular = ConsejoPopular.objects.first()
                per.save()
                p.datos_personales = per
                p.datos_usuario = instance
                p.save()
