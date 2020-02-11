from django.urls import path
from .views import *

urlpatterns = [
   path('', index, name='quejas_list'),
   path('add', agregar_queja, name='quejas_add'),
   path('edit/<int:id_queja>', index, name='quejas_edit'),
   path('del/<int:id_queja>', index, name='quejas_del'),
   path('<int:id_queja>', index, name='quejas_detail'),
   path('depto/<int:id_queja>', index, name='quejas_asig_depto'),
   path('tecnico/<int:id_queja>', index, name='quejas_asig_tec'),
   path('response/<int:id_queja>', index, name='quejas_response'),
   path('tecnico/<int:id_queja>', index, name='quejas_asig_tec'),
   path('response/<int:id_queja>', index, name='quejas_response'),
   path('jdepto/<int:id_queja>', index, name='quejas_ajdepto'),
   path('dirtor/<int:id_queja>', index, name='quejas_adtor'),
   path('notify/<int:id_queja>', index, name='quejas_notify'),
   path('depto_many/', index, name='quejas_asig_many_dpto'),
   path('tecnico_many/', index, name='quejas_asig_many_tec'),
   path('notify_many/', index, name='quejas_notify_many'),
   path('deny/<int:id_queja>', index, name='quejas_deny'),
   path('redirect/<int:id_queja>', index, name='quejas_redirct'),
]
