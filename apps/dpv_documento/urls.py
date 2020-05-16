from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='docs_index'),
    path('add/', index, name='docs_add'),
    path('edit/<int:id_doc>', index, name='docs_edit'),
    path('remove/<int:id_doc>', index, name='docs_delete'),
    path('<int:id_doc>', index, name='docs_detail'),

]
