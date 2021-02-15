from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from apps.dpv_nomencladores.models import Municipio, Calle
from apps.dpv_nomencladores.validators import only_letters, only_numbers
from apps.dpv_nomencladores.models import Genero, AreaTrabajo, CentroTrabajo, ConsejoPopular
from apps.dpv_base.mixins import LoggerMixin
from .validators import ci_validate


# Create your models here.
class Persona(LoggerMixin):
    nombre = models.CharField(max_length=30, validators=[MaxLengthValidator(30)])
    cpopular = models.ForeignKey(ConsejoPopular, on_delete=models.CASCADE, null=True,
                                 verbose_name="Consejo Popular", default='', blank=True,)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    direccion_calle = models.ForeignKey(Calle, on_delete=models.CASCADE, verbose_name="Calle", blank=True)
    direccion_numero = models.PositiveSmallIntegerField(blank=True, verbose_name="Número")
    telefono = models.CharField(max_length=8, verbose_name="Teléfono Fijo",
                                null=True, blank=True, validators=[MinLengthValidator(8),
                                                                   MaxLengthValidator(8),
                                                                   only_numbers])
    movil = models.CharField(max_length=8, verbose_name="Teléfono Movil",
                             null=True, blank=True, validators=[MinLengthValidator(8),
                                                                MaxLengthValidator(8),
                                                                only_numbers])
    email_address = models.EmailField(verbose_name="Correo Electrónico", null=True, blank=True)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        unique_together = ('movil', 'deleted_at')
        abstract = True

    def __str__(self):
        return self.nombre

    @property
    def get_email(self):
        return self.email_address or None


class PersonaNatural(Persona):
    nombre = models.CharField(max_length=30, validators=[MaxLengthValidator(30), only_letters])
    apellidos = models.CharField(max_length=50, validators=[MaxLengthValidator(50), only_letters])
    ci = models.CharField(max_length=11,
                          validators=[MinLengthValidator(11,
                                                         message="Este campo no puede tener menos de 11 caracteres"),
                                      MaxLengthValidator(11,
                                                         message="Este campo no puede tener más de 11 caracteres"),
                                      only_numbers, ci_validate, ], unique=True, verbose_name="CI")
    direccion_entrecalle1 = models.ForeignKey(Calle, related_name="persona_entrecalle1",
                                              on_delete=models.CASCADE, verbose_name="Primera Entrecalle", blank=True)
    direccion_entrecalle2 = models.ForeignKey(Calle, related_name="persona_entrecalle2",
                                              on_delete=models.CASCADE, verbose_name="Segunda Entrecalle", blank=True)
    genero = models.ForeignKey(Genero, verbose_name="Género", blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Persona Natural"
        verbose_name_plural = "Personas Naturales"
        ordering = ["ci", "apellidos", ]
        unique_together = ("ci", "deleted_at")

    def __str__(self):
        return '%s %s' % (self.nombre, self.apellidos)


class PersonaJuridica(Persona):
    nombre = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    sigla = models.CharField(max_length=15, verbose_name="Siglas",
                             blank=True, help_text="Siglas identificativas de la entidad.")
    nombre_contacto = models.CharField(max_length=200, verbose_name="Nombre de contacto", blank=True,
                                       help_text="Nombre que se usara para el contacto con la entidad.")
    codigo_nit = models.CharField(max_length=11, verbose_name="Código NiT", help_text="Código NiT de la entidad")
    codigo_reuup = models.CharField(max_length=11, verbose_name="Código Reeup", help_text="Código Reeup de la Entidad")
    direccion_entrecalle1 = models.ForeignKey(Calle, related_name="personaj_entrecalle1",
                                              on_delete=models.CASCADE, verbose_name="Primera Entrecalle", blank=True)
    direccion_entrecalle2 = models.ForeignKey(Calle, related_name="personaj_entrecalle2",
                                              on_delete=models.CASCADE, verbose_name="Segunda Entrecalle", blank=True)

    class Meta:
        verbose_name = "Persona Jurídica"
        verbose_name_plural = "Personas Jurídicas"
        unique_together = (("codigo_nit", "deleted_at"), ("codigo_reuup", "deleted_at"), ("nombre", "deleted_at"))

    def __str__(self):
        return self.nombre
