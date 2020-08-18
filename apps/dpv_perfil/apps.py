from django.apps import AppConfig


class DpvPerfilConfig(AppConfig):
    name = 'apps.dpv_perfil'     # Nombre identificador del modulo tiene que cumplir con el estandar
    verbose_name = "Perfiles"    # Nombre de Humanizado del modulo sera utilizado para mostrar en el menu
    menu = ''              # Si el modulo se mostrara en el menu
    menuable = False    # Si el modulo se mostrara en el menu
    owned = True        # Si es una aplicacion nuestra
    active = True       # Si el modulo esta activo, es como si esta instalado
    parent = True      # Si el modulo es un submodulo de otro en el menu (y solo en el menu)
    child_of = ''     # Si el modulo es hijo de otro en el menu se coloca aqui el nombre(atributo name) del modulo padre
