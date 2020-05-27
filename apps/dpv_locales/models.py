from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from apps.dpv_base.mixins import LoggerMixin
from apps.dpv_nomencladores.models import Municipio, Organismo, Calle, Piso, ConsejoPopular
from .validators import validate_acta_acuerdo, start_with_number


# Create your models here.
registring = False


class Local(LoggerMixin):
    direccion_calle = models.ForeignKey(Calle, related_name="calle_principal", help_text="Calle de la direccion", on_delete=models.CASCADE, verbose_name="Calle", blank=False, null=False)
    direccion_numero = models.CharField(max_length=10, help_text="Numero de la dirección", verbose_name="Número", validators=[start_with_number])
    piso = models.ForeignKey(Piso, help_text="Piso de la direccion del local", on_delete=models.CASCADE)
    direccion_entre1 = models.ForeignKey(Calle, related_name="entrecalle1", verbose_name="Primera Entrecalle", max_length=50, help_text="Primera entre calle de la dirección", on_delete=models.CASCADE)
    direccion_entre2 = models.ForeignKey(Calle, related_name="entrecalle2", verbose_name="Segunda Entrecalle", max_length=50, help_text="Segunda entre calle de la dirección", on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, related_name="locales_mun", help_text="Municipio donde se encuentra ubicado el local el local", on_delete=models.CASCADE)
    no_viviendas = models.PositiveSmallIntegerField(verbose_name="Total de viviendas", help_text="Total de viviendas en el local", validators=[MaxValueValidator(50)])
    aprobado = models.BooleanField(default=False, help_text="Marque si está aprobado el local")
    pendiente = models.PositiveSmallIntegerField(verbose_name="Pendientes de aprobación", help_text="Viviendas pendientes de aprobación", validators=[MaxValueValidator(50)])
    organismo = models.ForeignKey(Organismo, help_text="Organismo que ocupa el local", related_name="locales_org", on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True, auto_created=True, help_text="Fecha en que se introdujo el local al sistema.")
    acta = models.CharField(max_length=9, validators=[validate_acta_acuerdo], verbose_name="Acta")
    acuerdoCAM = models.CharField(max_length=9, verbose_name="Acuerdo CAM", validators=[validate_acta_acuerdo], blank=True, default='')
    acuerdoPEM = models.CharField(max_length=9, verbose_name="Acuerdo PEM", validators=[validate_acta_acuerdo], blank=True, default='')
    acuerdoORG = models.CharField(max_length=9, verbose_name="Acuerdo Organismo", validators=[validate_acta_acuerdo], blank=True, default='')
    observaciones = models.TextField(max_length=600, verbose_name="Otras observaciones")
    estatal = models.BooleanField(default=True, verbose_name="Es estatal")
    acuerdo_DPV = models.CharField(max_length=9, verbose_name="Acuerdo DPV",  validators=[validate_acta_acuerdo], default='', blank=True)
    consejo_popular = models.ForeignKey(ConsejoPopular, default=None, on_delete=models.CASCADE, verbose_name="Consejo Popular", help_text="Consejo popular donde se encuetra ubicado el Local", blank=True, null=True)
    data_ok = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)])
    system_info = models.TextField(max_length=300, default='', blank=True)

    class Meta:
        verbose_name = "Local"
        ordering = ['fecha', ]
        verbose_name_plural = "Locales"
        unique_together = (('municipio', 'direccion_calle', 'direccion_numero', 'piso', ),)

    def __str__(self):
        return self.municipio.nombre + '-' + self.direccion_calle.nombre + ' # ' + self.direccion_numero

    def get_ok_data(self):
        validation_text = ''
        validation_point = 0
        validation_house_point = 0

        if self.no_viviendas != self.vivienda_local.count():
            validation_point += 1
            validation_text += "No coincide el número de viviendas declarado en el local que es %d con el número de viviendas asociadas al mismo que es %d. \n" % (self.no_viviendas, self.vivienda_local.count())
        for viv in self.vivienda_local.all():
            tmp_point = validation_point
            if not viv.numero:
                validation_text += "La " + str(self.vivienda_local.index(viv)) + " no tiene número. \n"
                validation_point += 1
            if not viv.destino:
                validation_text += "La vivienda " + str(viv.numero) + " le no tiene configurado el destino. \n"
                validation_point += 1
            if not viv.cantidad_persona:
                validation_text += "La vivienda " + str(viv.numero) + " le no tiene configurado la cantidad de personas que la habitan. \n"
                validation_point += 1
            if not viv.propietario:
                validation_text += "La vivienda " + str(viv.numero) + " le no tiene configurado el propietario. \n"
                validation_point += 1
            if not viv.fecha_propietario:
                validation_text += "La vivienda " + str(viv.numero) + " le no tiene configurado la fecha a partir de donde se conmenzo a habitar. \n"
                validation_point += 1
            if not viv.concepto:
                validation_text += "La vivienda " + str(viv.numero) + " le no tiene configurado el concepto. \n"
                validation_point += 1
            if not viv.aprobada:
                validation_text += "La vivienda " + str(viv.numero) + " no está aprobada."
                validation_point += 1
            if not viv.add_concepto:
                validation_text += "La vivienda " + str(viv.numero) + " le no tiene configurado el destino"
            if tmp_point > validation_point:
                validation_house_point += 1

        # Seteo las variables data_ok y system_info segun los errores encontrados
        if validation_point == 0:
            self.data_ok = validation_point
            self.system_info = "No existen errores o anomalías en la información de este local."
        if validation_point > 0 and self.vivienda_local.count() == 0:
            self.data_ok = 2
            self.system_info = "Este local no tiene viviendas asociadas."
        if validation_point > 0 and self.vivienda_local.count() > 0:
            if validation_point + validation_house_point < 3:
                self.data_ok = 1
                self.system_info = validation_text
            else:
                self.data_ok = 2
                self.system_info = validation_text

        self.save()

    def count_statal(self):
        if self.estatal:
            return 1
        else:
            return 0
