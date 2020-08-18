from django.apps import AppConfig


class DpvDocumentoConfig(AppConfig):
    name = 'apps.dpv_documento'  # Nombre identificador del modulo tiene que cumplir con el estandar
    verbose_name = "Documentos"  # Nombre de Humanizado del modulo sera utilizado para mostrar en el menu
    menu = 'dpv_documento/menu/main_menu.html'  # Plantilla HTML de que se mostrara el modulo del menu
    menuable = True  # Si el modulo se mostrara en el menu
    owned = True  # Si es una aplicacion nuestra
    active = True  # Si el modulo esta activo, es como si esta instalado
    parent = True  # Si el modulo es un submodulo de otro en el menu (y solo en el menu)
    child_of = ''  # Si el modulo es hijo de otro en el menu se coloca aqui el nombre(atributo name) del modulo padre
    model_data = ['DPVDocumento']
    name_data = 'Documentos Registrados'  # Nombre o texto a mostrar del sisginificado de dichos registros
    route_data = 'list_docs'  # ruta principal del modulo
    main_permission = 'dpv_documento.view_dpvdocumento'

    def ready(self):
        pass
