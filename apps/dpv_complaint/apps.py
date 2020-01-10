from django.apps import AppConfig


class DpvComplaintConfig(AppConfig):
    name = 'apps.dpv_complaint'
    verbose_name = "Quejas"     # Nombre de Humanizado del modulo sera utilizado para mostrar en el menu
    menu = 'dpv_complaint/menu/main_menu.html'  # Plantilla HTML de que se mostrara el modulo del menu
    menuable = True    # Si el modulo se mostrara en el menu
    owned = True        # Si es una aplicacion nuestra
    active = True       # Si el modulo esta activo, es como si esta instalado
    parent = True      # Si el modulo es un submodulo de otro en el menu (y solo en el menu)
    child_of = ''     # Si el modulo es hijo de otro en el menu se coloca aqui el nombre(atributo name) del modulo padre
    route_data = 'index_natural_complaint'
    model_data = ['Complaint']
    name_data = 'Quejas Registrados'