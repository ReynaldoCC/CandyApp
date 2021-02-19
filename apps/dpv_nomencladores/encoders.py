from django.core.serializers.json import DjangoJSONEncoder

from .models import Municipio


class CustomNomenclatorEncoder(DjangoJSONEncoder):
    """
    Custom encoder to code nomenclator models to json already parsed
    Municipio
    """
    def default(self, o):
        if isinstance(o, Municipio):
            try:
                return {"id": o.id, "nombre": o.nombre}
            except TypeError as e:
                super(self, CustomNomenclatorEncoder).default(o)
