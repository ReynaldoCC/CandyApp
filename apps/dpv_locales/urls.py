from django.urls import path
from .views import index, stats, local_add, local_edit, local_detail, local_remove, local_revision, local_systeminfo, \
    local_verify, local_detail_full

urlpatterns = [
    path('', index, name='locales_list'),
    path('estadistico/', stats, name='locales_stats'),
    path('estadistico/<int:id_municipio>', stats, name='locales_stats_mun'),
    path('estadistico/<int:id_municipio>/<int:id_cpopular>', stats, name='locales_stats_cpop'),
    path('form/', local_add, name='locales_add'),
    path('form/<int:id_local>', local_edit, name='locales_edit'),
    path('updt/', local_revision, name='locales_revs'),
    path('updt/<int:id_local>', local_revision, name='locales_rev'),
    path('system/<int:id_local>', local_systeminfo, name='locales_data'),
    path('view/<int:id_local>', local_detail, name='locales_view'),
    path('delete/<int:id_local>', local_remove, name='locales_delete'),
    path('view/page/<int:id_local>', local_detail_full, name='locales_view_page'),
    path('verify', local_verify, name='locales_verify'),

]
