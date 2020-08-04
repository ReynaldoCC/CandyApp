from django.apps import AppConfig
# from .models import Vivienda


class DpvViviendasConfig(AppConfig):
    name = 'apps.dpv_viviendas'       # Nombre identificador del modulo tiene que cumplir con el estandar
    verbose_name = "Viviendas"      # Nombre de Humanizado del modulo sera utilizado para mostrar en el menu
    menu = 'dpv_viviendas/menu/main_menu.html'  # Plantilla HTML de que se mostrara el modulo del menu
    menuable = False    # Si el modulo se mostrara en el menu
    owned = True        # Si es una aplicacion nuestra
    active = True       # Si el modulo esta activo, es como si esta instalado
    parent = False      # Si el modulo es un submodulo de otro en el menu (y solo en el menu)
    child_of = 'apps.dpv_locales'     # Si el modulo es hijo de otro en el menu se coloca aqui el nombre(atributo name) del modulo padre
    # count_data = Vivienda.objects.all().count() # Cantidad de registros del elemento funcamental del modulo o app
    model_data = ['Vivienda']
    name_data = 'Viviendas Registradas' # Nombre o texto a mostrar del sisginificado de dichos registros
    route_data = 'vivienda_list' # ruta principal del modulo