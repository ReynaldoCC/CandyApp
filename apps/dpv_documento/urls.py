from django.urls import path
from .views import (
    list_typedocs,
    create_typedocs,
    update_typedocs,
    delete_typedocs,
    list_docs,
    create_doc,
)

urlpatterns = [
    # TIPO DE DOCUMENTOS
    path('tipos/', list_typedocs, name='list_typedocs'),
    path('tipos/add/', create_typedocs, name='typedocs_add'),
    path('tipos/edit/<int:typedoc_id>/', update_typedocs, name='typedocs_edit'),
    path('tipos/remove/<int:typedoc_id>/', delete_typedocs, name='typedocs_delete'),
    # DOCUMENTOS
    path('', list_docs, name='list_docs'),
    path('add/', create_doc, name='docs_add'),
    path('edit/<int:id_doc>/', list_docs, name='docs_edit'),
    path('remove/<int:id_doc>/', list_docs, name='docs_delete'),
    path('<int:id_doc>/', list_docs, name='docs_detail'),

]
