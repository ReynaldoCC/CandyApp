from django.apps import AppConfig
# from .models import PersonaNatural


class DpvPersonaConfig(AppConfig):
    name = 'apps.dpv_persona'  # Nombre identificador del modulo tiene que cumplir con el estandar
    verbose_name = "Personas"  # Nombre de Humanizado del modulo sera utilizado para mostrar en el menu
    menu = 'dpv_persona/menu/main_menu.html'  # Plantilla HTML de que se mostrara el modulo del menu
    menuable = True    # Si el modulo se mostrara en el menu
    owned = True        # Si es una aplicacion nuestra
    active = True       # Si el modulo esta activo, es como si esta instalado
    parent = False      # Si el modulo es un submodulo de otro en el menu (y solo en el menu)
    child_of = 'apps.dpv_nomencladores'     # Si el modulo es hijo de otro en el menu se coloca aqui el nombre(atributo name) del modulo padre
    # count_data = PersonaNatural.objects.all().count() # Cantidad de registros del elemento funcamental del modulo o app
    model_data = ['PersonaNatural']
    name_data = 'Personas Registradas'  # Nombre o texto a mostrar del sisginificado de dichos registros
    route_data = 'persona_natural'  # ruta principal del modulo
    main_permission = 'dpv_persona.view_personanatural'
