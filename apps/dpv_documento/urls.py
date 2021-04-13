from django.urls import path
from .views import *

urlpatterns = [
    # TIPO DE DOCUMENTOS
    path('tipos/', list_typedocs, name='list_typedocs'),
    path('tipos/add/', create_typedocs, name='typedocs_add'),
    path('tipos/edit/<int:typedoc_id>/', update_typedocs, name='typedocs_edit'),
    path('tipos/remove/<int:typedoc_id>/', delete_typedocs, name='typedocs_delete'),
    path('tipos/filter/<int:typedoc_id>/', typedoc_filter_con_respuesta, name='typedoc_filter_con_respuesta'),
    # DOCUMENTOS
    path('', list_docs, name='list_docs'),
    path('resumen/', resume_docs, name='resume_docs'),
    path('detail/<int:doc_id>/', detail_doc, name='doc_detail'),
    path('add/', create_doc, name='docs_add'),
    path('edit/<int:doc_id>/', update_doc, name='docs_edit'),
    path('setdate/<int:doc_id>/', setdate_doc, name='docs_setdate'),
    path('remove/<int:doc_id>/', delete_docs, name='docs_delete'),
]
