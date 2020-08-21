from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_init
from django.dispatch import receiver
from .validators import only_numbers, only_letters, not_special_char, not_letters
from django.core.validators import MaxLengthValidator, MinLengthValidator, EmailValidator, URLValidator
from apps.dpv_base.mixins import LoggerMixin
import uuid


# Create your models here.
def scramble_upload_logo(instance, filename, subdiretory='logos'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


class Provincia(LoggerMixin):
    nombre = models.CharField(max_length=30, help_text="Nombre del municipio", verbose_name="Provincia",
                              validators=[not_special_char, MaxLengthValidator(30)])
    numero = models.CharField(max_length=2, verbose_name="Número", validators=[only_numbers])

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ["numero", ]
        unique_together = (('nombre', 'deleted_at'), ('numero', 'deleted_at'))

    def __str__(self):
        return self.nombre


class Municipio(LoggerMixin):
    nombre = models.CharField(max_length=90, help_text="Nombre del municipio",
                              verbose_name="Municipio", validators=[not_special_char, MaxLengthValidator(90)])
    numero = models.CharField(max_length=2, verbose_name="Número", validators=[only_numbers])
    provincia = models.ForeignKey(Provincia, related_name="municipios", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['numero', ]
        unique_together = (('nombre', 'deleted_at'), ('numero', 'deleted_at'))

    def __str__(self):
        return self.nombre


class ConsejoPopular(LoggerMixin):
    nombre = models.CharField(max_length=90, help_text="Nombre del consejo popular",
                              verbose_name="Consejo Popular", blank=False, null=False,
                              validators=[not_special_char, MaxLengthValidator(90)])
    numero = models.CharField(max_length=2, verbose_name="Número", validators=[only_numbers])
    municipio = models.ForeignKey(Municipio, related_name="consejos", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Consejo Popular"
        verbose_name_plural = "Consejos Populares"
        ordering = ['numero', ]
        unique_together = (('nombre', 'deleted_at'), ('numero', 'deleted_at'))

    def __str__(self):
        return self.nombre


class Organismo(LoggerMixin):
    nombre = models.CharField(max_length=90, help_text=_("Nombre del organismo."), verbose_name=_("Organismo"),
                              validators=[not_special_char, MaxLengthValidator(90)])
    siglas = models.CharField(max_length=15, help_text=_("Siglas representativas del organismo"),
                              verbose_name=_("Siglas"), validators=[not_special_char])
    email = models.EmailField(verbose_name=_("Correo Electrónico"), blank=True, default="",
                              help_text=_("Correo eletrónico de contacto del organismo"))
    telefono = models.CharField(verbose_name=_("Teléfono"), blank=True, default="", max_length=8,
                                validators=[MinLengthValidator(8), MaxLengthValidator(8), only_numbers],
                                help_text=_("Teléfono de contacto del organismo"))
    nombre_contacto = models.CharField(verbose_name=_("Nombre de contacto"), blank=True, default="", max_length=200,
                                       validators=[MinLengthValidator(3), MaxLengthValidator(200), only_letters],
                                       help_text=_("Nombre de la persona de contacto del organismo"))

    class Meta:
        verbose_name = "Organismo"
        verbose_name_plural = "Organismos"
        ordering = ['nombre', ]
        unique_together = (('nombre', 'deleted_at'), ('email', 'deleted_at'), ('telefono', 'deleted_at'))

    def __str__(self):
        return self.nombre


class Destino(LoggerMixin):
    nombre = models.CharField(max_length=90, help_text="Identificador del destino",
                              verbose_name="Destino", validators=[not_special_char, MaxLengthValidator(90)])

    class Meta:
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"
        ordering = ['nombre', ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class Calle(LoggerMixin):
    nombre = models.CharField(max_length=90, help_text="Nombre de la calle", verbose_name="Nombre",
                              validators=[not_special_char, MaxLengthValidator(90)])
    municipios = models.ManyToManyField(Municipio, default='', blank=True, verbose_name='Municipios',
                                        help_text='Municipios en los que esta presente una calle con este nombre.')

    class Meta:
        verbose_name = "Calle"
        verbose_name_plural = "Calles"
        ordering = ['nombre', ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class Piso(LoggerMixin):
    nombre = models.CharField(max_length=20, help_text="Nombre del piso", verbose_name="Piso",
                              validators=[not_special_char])

    class Meta:
        verbose_name = "Piso"
        verbose_name_plural = "Pisos"
        ordering = ['nombre', ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class CentroTrabajo(LoggerMixin):
    nombre = models.CharField(max_length=100, verbose_name="Centro de trabajo",
                              validators=[MaxLengthValidator(100), not_special_char],
                              help_text="Nombre de la unidad.")
    siglas = models.CharField(max_length=15, verbose_name="Siglas",
                              validators=[MaxLengthValidator(7), not_special_char],
                              help_text="Siglas de la entidad.")
    numero = models.CharField(max_length=3, verbose_name="Número", blank=True,
                              help_text="Número de la unidad", validators=[only_numbers, MaxLengthValidator(3)])
    oc = models.BooleanField(default=False, verbose_name="Oficina Central",
                             help_text="Indica si la unidad es la oficina central")
    municipio = models.ForeignKey(Municipio, related_name="ubicacion_work",
                                  on_delete=models.CASCADE, help_text="Municipio donde está ubicado el centro.")

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
        ordering = ["numero", "nombre", ]
        unique_together = (('nombre', 'deleted_at'), ('numero', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class AreaTrabajo(LoggerMixin):
    nombre = models.CharField(max_length=90, verbose_name="Área de Trabajo",
                              validators=[MaxLengthValidator(90), not_special_char])
    numero = models.CharField(max_length=2, verbose_name="Número", validators=[only_numbers])

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), ('numero', 'deleted_at'))

    def __str__(self):
        return self.nombre


class Organizacion(LoggerMixin):
    nombre = models.CharField(max_length=90, verbose_name="Organización",
                              validators=[MaxLengthValidator(90), not_special_char])
    siglas = models.CharField(max_length=15, verbose_name="Siglas", default="",
                              validators=[MaxLengthValidator(10), not_special_char])
    email = models.EmailField(verbose_name=_("Correo Electrónico"), blank=True, default="",
                              help_text=_("Correo eletrónico de contacto de la prensa"))
    telefono = models.CharField(verbose_name=_("Teléfono"), blank=True, default="", max_length=8,
                                validators=[MinLengthValidator(8), MaxLengthValidator(8), only_numbers],
                                help_text=_("Teléfono de contacto de la organización"))
    nombre_contacto = models.CharField(verbose_name=_("Nombre de contacto"), blank=True, default="", max_length=200,
                                       validators=[MinLengthValidator(3), MaxLengthValidator(200), only_letters],
                                       help_text=_("Nombre de la persona de contacto de la organización"))

    class Meta:
        verbose_name = "Organización"
        verbose_name_plural = "Organizaciones"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class Genero(LoggerMixin):
    nombre = models.CharField(max_length=11, verbose_name="Género",
                              validators=[MaxLengthValidator(11), only_letters])
    sigla = models.CharField(max_length=1, verbose_name="Inicial",
                             validators=[MinLengthValidator(1), MaxLengthValidator(1), only_letters])

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        ordering = ['nombre', ]
        unique_together = (('nombre', 'deleted_at'), ('sigla', 'deleted_at'))

    def __str__(self):
        return self.nombre


class Concepto(LoggerMixin):
    nombre = models.CharField(max_length=40, verbose_name="Concepto", validators=[not_special_char])

    class Meta:
        verbose_name = "Concepto"
        verbose_name_plural = "Conceptos"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class CodificadorAsunto(LoggerMixin):
    nombre = models.CharField(max_length=250, verbose_name="Codificador de Asunto",
                              validators=[MaxLengthValidator(250), not_special_char])
    numero = models.CharField(max_length=3, verbose_name="Número", validators=[only_numbers])

    class Meta:
        verbose_name = "Codificador de Asunto"
        verbose_name_plural = "Codificadores de Asuntos"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), ('numero', 'deleted_at'))

    def __str__(self):
        return '({}) - {}'.format(self.numero, self.nombre)


class TipoQueja(LoggerMixin):
    nombre = models.CharField(max_length=50, verbose_name="Tipo de Queja",
                              validators=[MaxLengthValidator(50), not_special_char])
    numero = models.CharField(max_length=3, verbose_name="Código", validators=[not_letters])

    class Meta:
        verbose_name = "Tipo de Queja"
        verbose_name_plural = "Tipos de las Quejas"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), ('numero', 'deleted_at'))

    def __str__(self):
        return self.nombre


class PrensaEscrita(LoggerMixin):
    nombre = models.CharField(max_length=90, verbose_name="Prensa Escrita",
                              validators=[MaxLengthValidator(90), not_special_char])
    siglas = models.CharField(max_length=15, verbose_name="Siglas",
                              validators=[MaxLengthValidator(10), not_special_char])
    email = models.EmailField(verbose_name=_("Correo Electrónico"), blank=True, default="",
                              help_text=_("Correo eletrónico de contacto de la prensa"))
    telefono = models.CharField(verbose_name=_("Teléfono"), blank=True, default="", max_length=8,
                                validators=[MinLengthValidator(8), MaxLengthValidator(8), only_numbers],
                                help_text=_("Teléfono de contacto de la prensa"))
    nombre_contacto = models.CharField(verbose_name=_("Nombre de contacto"), blank=True, default="", max_length=200,
                                       validators=[MinLengthValidator(3), MaxLengthValidator(200), only_letters],
                                       help_text=_("Nombre de la persona de contacto de la prensa"))

    class Meta:
        verbose_name = "Prensa Escrita"
        verbose_name_plural = "Prensas Escritas"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class Email(LoggerMixin):
    email = models.EmailField(max_length=255, verbose_name="Correo Electrónico",
                              validators=[MaxLengthValidator(255), EmailValidator()])

    class Meta:
        verbose_name = "Correo Electrónico"
        verbose_name_plural = "Correos Electrónicos"
        ordering = ["email", ]
        unique_together = (('email', 'deleted_at'), )

    def __str__(self):
        return self.email


class Telefono(LoggerMixin):
    numero = models.CharField(max_length=11, verbose_name="Teléfono",
                              validators=[MaxLengthValidator(11), not_special_char])

    class Meta:
        verbose_name = "Teléfono"
        verbose_name_plural = "Teléfonos"
        ordering = ["numero", ]
        unique_together = (('numero', 'deleted_at'), )

    def __str__(self):
        return self.numero


class TipoProcedencia(LoggerMixin):
    nombre = models.CharField(max_length=90, verbose_name="Tipo de Procedencia",
                              validators=[MaxLengthValidator(90), not_special_char])
    cant_dias = models.PositiveSmallIntegerField(verbose_name="Días para Respuesta")
    enviar = models.BooleanField(default=True, verbose_name="Enviar Respuesta",
                                 help_text="Marque para enviar la respuesta por correo electrónico")

    class Meta:
        verbose_name = "Tipo de Procedencia"
        verbose_name_plural = "Tipos de Procedencias"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class RedSocial(LoggerMixin):
    nombre = models.CharField(verbose_name=_("Nombre"), blank=True, default="", max_length=25,
                              validators=[MinLengthValidator(3), MaxLengthValidator(25)],
                              help_text=_("Nombre de la red social"))
    dominio = models.CharField(verbose_name=_("URL"), blank=True, default="", max_length=254,
                               validators=[MinLengthValidator(3), MaxLengthValidator(254), URLValidator],
                               help_text=_("URL del dominio de la red social")),
    logo = models.ImageField('Logo', upload_to=scramble_upload_logo, blank=True, null=True)

    class Meta:
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), )


class ProcedenciaWeb(LoggerMixin):
    nombre = models.CharField(verbose_name=_("Nombre"), blank=True, default="", max_length=200,
                              validators=[MinLengthValidator(3), MaxLengthValidator(200), only_letters],
                              help_text=_("Nombre de la persona o Perfil"))
    perfil = models.CharField(verbose_name=_("Perfil Social"), blank=True, default="", max_length=200,
                              validators=[MinLengthValidator(3), MaxLengthValidator(200), only_letters],
                              help_text=_("Idetntificador del perfil social"))
    email = models.EmailField(verbose_name=_("Correo Electrónico"), blank=True, default="",
                              help_text=_("Correo eletrónico del perfil"))
    red_social = models.ForeignKey(RedSocial, on_delete=models.CASCADE, verbose_name=_("Red Social"), blank=True,
                                   default="", help_text=_("Red social a la que pertenece el perfil."))

    class Meta:
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"
        ordering = ["nombre", ]
        unique_together = (('perfil', 'email', 'red_social', 'deleted_at'), )


class Procedencia(LoggerMixin):
    nombre = models.CharField(max_length=50, verbose_name="Procedencia",
                              validators=[MaxLengthValidator(50), not_special_char])
    tipo = models.ForeignKey(TipoProcedencia, related_name="procedencias",
                             on_delete=models.CASCADE, default='', blank=True)
    limit = models.Q(app_label='dpv_nomencladores', model='organismo') | \
        models.Q(app_label='dpv_nomencladores', model='organizacion') | \
        models.Q(app_label='dpv_nomencladores', model='prensaescrita') | \
        models.Q(app_label='dpv_nomencladores', model='telefono') | \
        models.Q(app_label='dpv_nomencladores', model='email') | \
        models.Q(app_label='dpv_nomencladores', model='procedenciaweb') | \
        models.Q(app_label='dpv_persona', model='personanatural') | \
        models.Q(app_label='dpv_persona', model='personajuridica')
    tipo_contenido = models.ForeignKey(ContentType, verbose_name=_('Contenido de Procedencia'),
                                       limit_choices_to=limit,
                                       null=True, blank=True, on_delete=models.CASCADE)
    id_objecto = models.PositiveIntegerField(verbose_name=_('related object'), null=True)
    objecto_contenido = GenericForeignKey('tipo_contenido', 'id_objecto')

    class Meta:
        verbose_name = "Procedencia"
        verbose_name_plural = "Procedencias"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class Estado(LoggerMixin):
    nombre = models.CharField(max_length=90, verbose_name="Estado de la Queja",
                              validators=[MaxLengthValidator(90), not_special_char])

    class Meta:
        verbose_name = "Estado de la Queja"
        verbose_name_plural = "Estados de las Quejas"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class ClasificacionRespuesta(LoggerMixin):
    nombre = models.CharField(max_length=90, verbose_name="Clasificación de la Respuesta",
                              validators=[MaxLengthValidator(90), not_special_char])
    codigo = models.CharField(max_length=5, verbose_name="Código", validators=[only_letters])

    class Meta:
        verbose_name = "Clasificación de la Respuesta"
        verbose_name_plural = "Clasificaciones de las Respuestas"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), ('codigo', 'deleted_at'))

    def __str__(self):
        return self.nombre


class ConclusionCaso(LoggerMixin):
    nombre = models.CharField(max_length=90, verbose_name="Conclusión del Caso",
                              validators=[MaxLengthValidator(90), not_special_char])
    codigo = models.CharField(max_length=3, verbose_name="Código", validators=[only_letters])

    class Meta:
        verbose_name = "Conclusión del Caso"
        verbose_name_plural = "Conclusiones del Casos"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), ('codigo', 'deleted_at'))

    def __str__(self):
        return self.codigo


class RespuestaAQueja(LoggerMixin):
    nombre = models.CharField(max_length=100, verbose_name=_("Respuesta a"),
                              help_text=_("A quien se le debe enviar o notificar la respuesta."),
                              validators=[MaxLengthValidator(100), ])

    class Meta:
        verbose_name = "Respuesta a"
        verbose_name_plural = "Respuestas a"
        ordering = ["nombre", ]
        unique_together = (('nombre', 'deleted_at'), )

    def __str__(self):
        return self.nombre


class Anonimo(models.Model):
    name = models.CharField(verbose_name=_('Anónimo'), max_length=8, default='Anónimo', blank=False, null=False)

    class Meta:
        verbose_name = 'Anónimo'
        verbose_name_plural = 'Anónimos'

    def __str__(self):
        return 'Anónimo'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Anonimo.objects.exists():
            self.id = Anonimo.objects.first().id
            self.name = Anonimo.objects.first().name
            super(Anonimo, self).save()
        else:
            super(Anonimo, self).save(force_insert=False, force_update=False, using=None,
                                      update_fields=None)


def configurar_nombre_procedencia(instance):
    if not instance or instance is None:
        return
    try:
        if not instance.nombre or instance.nombre == "":
            nuevo_nombre = "({}) {}".format(instance.tipo.nombre, instance.objecto_contenido.__str__())
            instance.nombre = nuevo_nombre[:50]
    except ValueError as e:
        print(str(e))


def configurar_tipo_procedencia(instance):
    if not instance or instance is None:
        return
    try:
        # if not instance.tipo or instance.tipo is None:
        if instance.tipo_contenido.model == "personanatural":
            instance.tipo = TipoProcedencia.objects.get(id=3)
        elif instance.tipo_contenido.model == "personajuridica":
            instance.tipo = TipoProcedencia.objects.get(id=6)
        elif instance.tipo_contenido.model == "organizacion":
            instance.tipo = TipoProcedencia.objects.get(id=8)
        elif instance.tipo_contenido.model == "prensaescrita":
            instance.tipo = TipoProcedencia.objects.get(id=2)
        elif instance.tipo_contenido.model == "telefono":
            instance.tipo = TipoProcedencia.objects.get(id=4)
        elif instance.tipo_contenido.model == "gobierno":
            instance.tipo = TipoProcedencia.objects.get(id=7)
        elif instance.tipo_contenido.model == "email":
            instance.tipo = TipoProcedencia.objects.get(id=5)
        else:
            instance.tipo = TipoProcedencia.objects.get(id=1)
    except ValueError as e:
        print(str(e))


@receiver(pre_save, sender=Procedencia)
def preset_procedencia(sender, **kwargs):
    if kwargs.get('instance'):
        instance = kwargs.get('instance')
        configurar_tipo_procedencia(instance)
        configurar_nombre_procedencia(instance)
