from django.urls import path
from .views import index, vivienda_add, vivienda_edit, vivienda_detail, vivienda_delete, vivienda_add_modal

urlpatterns = [
    path('', index, name='vivienda_list'),
    path('form/', vivienda_add, name='vivienda_add'),
    path('formodal/<int:id_local>', vivienda_add_modal, name='vivienda_add_mod'),
    path('form/<int:id_vivienda>', vivienda_edit, name='vivienda_edit'),
    path('view/<int:id_vivienda>', vivienda_detail, name='vivienda_view'),
    path('delete/<int:id_vivienda>', vivienda_delete, name='vivienda_remove'),
]