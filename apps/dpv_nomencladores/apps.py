from django.apps import AppConfig
# from .models import ConsejoPopular


class DpvNomencladoresConfig(AppConfig):
    name = 'apps.dpv_nomencladores'      # Nombre identificador del modulo tiene que cumplir con el estandar
    verbose_name = "Nomencladores"     # Nombre de Humanizado del modulo sera utilizado para mostrar en el menu
    menu = 'dpv_nomencladores/menu/main_menu.html'  # Plantilla HTML de que se mostrara el modulo del menu
    menuable = True    # Si el modulo se mostrara en el menu
    owned = True        # Si es una aplicacion nuestra
    active = True       # Si el modulo esta activo, es como si esta instalado
    parent = True      # Si el modulo es un submodulo de otro en el menu (y solo en el menu)
    child_of = ''     # Si el modulo es hijo de otro en el menu se coloca aqui el nombre(atributo name) del modulo padre
    model_data = ['ConsejoPopular']
    name_data = 'Consejos Populares Registrados' # Nombre o texto a mostrar del sisginificado de dichos registros
    route_data = 'nomenclador_index' # ruta principal del modulo

    def ready(self):
        from .utils import charge_initial
        charge_initial()