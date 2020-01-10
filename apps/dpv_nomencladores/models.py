from django.db import models
from .validators import only_numbers, only_letters, not_numbers, not_letters, not_special_char
from django.core.validators import MaxLengthValidator, MinLengthValidator


# Create your models here.
class Provincia(models.Model):
    nombre = models.CharField(max_length=30, help_text="Nombre del municipio", verbose_name="Provincia", unique=True, validators=[not_special_char])
    numero = models.CharField(max_length=2, verbose_name="Número", unique=True, validators=[only_numbers])

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ["numero", ]

    def __str__(self):
        return  self.nombre


class Municipio(models.Model):
    nombre = models.CharField(max_length=30, help_text="Nombre del municipio", verbose_name="Municipio", unique=True, validators=[not_special_char])
    numero = models.CharField(max_length=2, verbose_name="Número", unique=True, validators=[only_numbers])
    provincia = models.ForeignKey(Provincia, related_name="municipios", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['numero', ]

    def __str__(self):
        return self.nombre


class ConsejoPopular(models.Model):
    nombre = models.CharField(max_length=30, help_text="Nombre del consejo popular", verbose_name="Consejo Popular", blank=False, null=False, unique=True, validators=[not_special_char])
    numero = models.CharField(max_length=2, verbose_name="Número", unique=True, validators=[only_numbers])
    municipio = models.ForeignKey(Municipio, related_name="municipios", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Consejo Popular"
        verbose_name_plural = "Consejos Populares"
        ordering = ['numero', ]

    def __str__(self):
        return self.nombre


class Organismo(models.Model):
    nombre = models.CharField(max_length=50, help_text="Nombre del organismo.", verbose_name=" Organismo", unique=True, validators=[not_special_char])
    siglas = models.CharField(max_length=7, help_text="Siglas representativas del organismo", unique=True, validators=[not_special_char])

    class Meta:
        verbose_name = "Organismo"
        verbose_name_plural = "Organismos"
        ordering = ['nombre', ]

    def __str__(self):
        return self.nombre


class Destino(models.Model):
    nombre = models.CharField(max_length=50, help_text="Identificador del destino", verbose_name="Destino", unique=True, validators=[not_special_char])

    class Meta:
        verbose_name = "Destino"
        verbose_name_plural = "Destinos"
        ordering = ['nombre', ]

    def __str__(self):
        return self.nombre


class Calle(models.Model):
    nombre = models.CharField(max_length=50, help_text="Nombre de la calle", verbose_name="Nombre", unique=True, validators=[not_special_char])
    municipios = models.ManyToManyField(Municipio, default='', blank=True, verbose_name='Municipios', help_text='Municipios en los que esta presente una calle con este nombre.')

    class Meta:
        verbose_name = "Calle"
        verbose_name_plural = "Calles"
        ordering = ['nombre', ]

    def __str__(self):
        return self.nombre


class Piso(models.Model):
    nombre = models.CharField(max_length=20, help_text="Nombre del piso", verbose_name="Piso", unique=True, validators=[not_special_char])

    class Meta:
        verbose_name = "Piso"
        verbose_name_plural = "Pisos"
        ordering = ['nombre', ]

    def __str__(self):
        return self.nombre


class CentroTrabajo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Centro de trabajo", unique=True, validators=[MaxLengthValidator(50), not_special_char], help_text="Nombre de la unidad.")
    siglas = models.CharField(max_length=5, verbose_name="Siglas", validators=[MaxLengthValidator(5), not_special_char], help_text="Siglas de la entidad.")
    numero = models.CharField(max_length=2, verbose_name="Número", blank=True, help_text="Número de la unidad", validators=[only_numbers, MaxLengthValidator(2)])
    oc = models.BooleanField(default=False, verbose_name="Oficina Central", help_text="Indica si la unidad es la oficina central")
    municipio = models.ForeignKey(Municipio, related_name="ubicacion_work", on_delete=models.CASCADE, help_text="Municipio donde está ubicado el centro.")

    class Meta:
        verbose_name = "Unidad"
        verbose_name_plural = "Unidades"
        ordering = ["numero", "nombre", ]

    def __str__(self):
        return self.nombre


class AreaTrabajo(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Área de Trabajo", unique=True, validators=[MaxLengthValidator(50), not_special_char])
    numero = models.CharField(max_length=2, verbose_name="Número", unique=True, validators=[only_numbers])

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ["nombre", ]

    def __str__(self):
        return self.nombre


class Genero(models.Model):
    nombre = models.CharField(max_length=9, verbose_name="Género", unique=True, validators=[MaxLengthValidator(9),
                                                                                            only_letters])
    sigla = models.CharField(max_length=1, verbose_name="Inicial", unique=True, validators=[MinLengthValidator(1),
                                                                                            MaxLengthValidator(1),
                                                                                            only_letters])

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"
        ordering = ['nombre', ]

    def __str__(self):
        return self.nombre


class Concepto(models.Model):
    nombre = models.CharField(max_length=25, verbose_name="Concepto", validators=[not_special_char])

    class Meta:
        verbose_name = "Concepto"
        verbose_name_plural = "Conceptos"
        ordering = ["nombre", ]

    def __str__(self):
        return self.nombre


class CodificadorAsunto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Codificador de Asunto", unique=True, validators=[MaxLengthValidator(150), not_special_char])
    numero = models.CharField(max_length=3, verbose_name="Número", unique=True, validators=[only_numbers])

    class Meta:
        verbose_name = "Codificador de Asunto"
        verbose_name_plural = "Codificadores de Asuntos"
        ordering = ["nombre", ]

    def __str__(self):
        return self.nombre


class TipoQueja(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Tipo de Queja", unique=True, validators=[MaxLengthValidator(50), not_special_char])
    numero = models.CharField(max_length=3, verbose_name="Código", unique=True, validators=[only_letters])

    class Meta:
        verbose_name = "Tipo de Queja"
        verbose_name_plural = "Tipos de las Quejas"
        ordering = ["nombre", ]

    def __str__(self):
        return self.nombre


class TipoProcedencia(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Tipo de Procedencia", unique=True, validators=[MaxLengthValidator(50), not_special_char])
    cant_dias = models.PositiveSmallIntegerField(verbose_name="Días para Respuesta")

    class Meta:
        verbose_name = "Tipo de Procedencia"
        verbose_name_plural = "Tipos de Procedencias"
        ordering = ["nombre", ]

    def __str__(self):
        return self.nombre

class Procedencia(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Procedencia", unique=True, validators=[MaxLengthValidator(50), not_special_char])
    enviar = models.BooleanField(default=True, verbose_name="Enviar Respuesta", help_text="Marque para enviar la respuesta por correo electrónico")
    tipo = models.OneToOneField(TipoProcedencia, related_name="municipios", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Procedencia"
        verbose_name_plural = "Procedencias"
        ordering = ["nombre", ]

    def __str__(self):
        return self.nombre


class Estado(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Estado de la Queja", unique=True, validators=[MaxLengthValidator(50), not_special_char])

    class Meta:
        verbose_name = "Estado de la Queja"
        verbose_name_plural = "Estados de las Quejas"
        ordering = ["nombre", ]

    def __str__(self):
        return self.nombre


class ClasificacionRespuesta(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Clasificación de la Respuesta", unique=True, validators=[MaxLengthValidator(50), not_special_char])
    codigo = models.CharField(max_length=3, verbose_name="Código", unique=True, validators=[only_letters])

    class Meta:
        verbose_name = "Clasificación de la Respuesta"
        verbose_name_plural = "Clasificaciones de las Respuestas"
        ordering = ["nombre", ]

    def __str__(self):
        return self.nombre