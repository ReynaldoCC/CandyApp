from django.apps import AppConfig


class DpvNotificacionesConfig(AppConfig):
    name = 'apps.dpv_notificaciones'
    verbose_name = "NOtificaciones"  # Nombre de Humanizado del modulo sera utilizado para mostrar en el menu
    menu = ''  # Plantilla HTML de que se mostrara el modulo del menu
    menuable = False  # Si el modulo se mostrara en el menu
    owned = True  # Si es una aplicacion nuestra
    active = True  # Si el modulo esta activo, es como si esta instalado
    parent = True  # Si el modulo es un submodulo de otro en el menu (y solo en el menu)
    child_of = ''  # Si el modulo es hijo de otro en el menu se coloca aqui el nombre(atributo name) del modulo padre
    model_data = ['Notify']
    name_data = 'Notificaciones'  # Nombre o texto a mostrar del sisginificado de dichos registros
    route_data = 'list_notifies'  # ruta principal del modulo
    main_permission = 'dpv_documento.view_notify'