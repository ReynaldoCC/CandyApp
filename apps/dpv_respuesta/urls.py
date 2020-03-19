from django.urls import path
from .views import *

urlpatterns = [

    path('tecnico/', index_tecnico, name='nomenclador_tecnico'),
    path('nueva_tecnico/', add_tecnico, name='tecnico_new'),
    path('editar_tecnico/<int:id_tecnico>', update_tecnico, name='tecnico_edit'),
    path('eliminar_tecnico/<int:id_tecnico>', delete_tecnico, name='tecnico_delete'),

]
