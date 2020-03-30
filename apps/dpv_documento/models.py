from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from apps.dpv_base.mixins import LoggerMixin
from apps.dpv_persona.models import PersonaNatural
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.dpv_nomencladores.models import AreaTrabajo, Municipio, Procedencia, Calle, ConsejoPopular, RespuestaAQueja
from .utils import configurar_numero_registro
import uuid


# Create your models here.
def scramble_upload_doc(instance, filename, subdiretory='docs'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


class TipoDPVDocumento(LoggerMixin):
    nombre = models.CharField(verbose_name=_("Nombre"), max_length=20, blank=True, default="")

    class Meta:
        verbose_name = _("Tipo de Documento")
        verbose_name_plural = _("Tipos de Documentos")
        ordering = ("nombre", )
        unique_together = (("nombre", "deleted_at"), )


class DPVDocumento(LoggerMixin):
    no_registro = models.CharField(max_length=10, verbose_name=_("No. Registro"), blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name=_("Fecha de Registro"))
    no_refer = models.CharField(max_length=20, verbose_name=_("No. Referencia"), default="")
    procedencia = models.ForeignKey(Procedencia, blank=True, verbose_name=_("Procedencia"),
                                    help_text=_("De donde proviene el documento"), on_delete=models.CASCADE)
    promovente = models.ForeignKey(PersonaNatural, blank=True, on_delete=models.CASCADE, verbose_name=_("Promovente"))
    clasificacion = models.ForeignKey(TipoDPVDocumento, blank=True,
                                      on_delete=models.CASCADE, verbose_name=_("Clasificacion"))
    asunto = models.CharField(max_length=400, verbose_name=_("Asunto"), blank=True, default="")
    destino = models.ForeignKey(AreaTrabajo, blank=True,
                                on_delete=models.CASCADE, verbose_name=_("Destino"))
    fecha_entrega = models.DateTimeField(verbose_name=_("Fecha de Entrega al Destino"), null=True, default=None)
    fecha_termino = models.DateTimeField(verbose_name=_("Fecha de Termino"), null=True, default=None)
    dir_calle = models.ForeignKey(Calle, verbose_name=_("Direccion Calle"),
                                  null=True, blank=True, default="",
                                  on_delete=models.CASCADE, related_name="doc_dir_calle")
    dir_numero = models.CharField(max_length=8, verbose_name=_("Direccion Numero"), null=True, blank=True, default="")
    dir_entrecalle1 = models.ForeignKey(Calle, verbose_name=_("Direccion Primera entrecalle"),
                                        null=True, blank=True, default="",
                                        on_delete=models.CASCADE, related_name="doc_dir_entrecalle1")
    dir_entrecalle2 = models.ForeignKey(Calle, verbose_name=_("Direccion Segunda Entrecalle"),
                                        null=True, blank=True, default="",
                                        on_delete=models.CASCADE, related_name="doc_dir_entrecalle2")
    dir_cpopular = models.ForeignKey(ConsejoPopular, verbose_name=_("Direccion Consejo Popular"),
                                     null=True, blank=True, default="",
                                     on_delete=models.CASCADE, related_name="doc_dir_cpopular")
    respuesta_a = models.ForeignKey(RespuestaAQueja, verbose_name=_("Direccion Consejo Popular"),
                                    null=True, blank=True, default="",
                                    on_delete=models.CASCADE, related_name="doc_dir_cpopular")
    municipio = models.ForeignKey(Municipio, blank=True,
                                  on_delete=models.CASCADE, verbose_name=_("Municipio"))
    dias = models.PositiveSmallIntegerField(verbose_name=_("Dias"), default=0, blank=True)
    registrado_por = models.ForeignKey(User, blank=True,
                                       on_delete=models.CASCADE, verbose_name=_("Registrado por"))
    archivo_digital = models.FileField(upload_to=scramble_upload_doc, verbose_name=_("Copia en Digital"), blank=True)

    class Meta:
        verbose_name = _("Documento")
        verbose_name_plural = _("Documentos")
        ordering = ("-fecha_registro", "no_registro", )
        unique_together = (("no_registro", "deleted_at"), )


# signals
@receiver(pre_save, sender=DPVDocumento)
def preset_document(sender, **kwargs):
    if kwargs.get("instance"):
        instance = kwargs.get("instance")
        if not instance.no_registro:
            configurar_numero_registro(instance)
