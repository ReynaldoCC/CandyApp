from django.urls import path
from apps.dpv_events import views


app_name = "dpv_events"
urlpatterns = [
    #   TIPOEVENTO
    path('tipoevento/',views.TipoEventoView,name='tipoevento'),
    path('create_tipoevento/', views.create_tipoevento, name='create_tipoevento'),
    path('update_tipoevento/', views.update_tipoevento, name='update_tipoevento'),
    path('delete_tipoevento/<int:tipoevento_id>/', views.delete_tipoevento, name='delete_tipoevento'),

    #   FRECUENCIA
    path('frecuencia/',views.FrecuenciaView,name='frecuencia'),
    path('create_frecuencia/', views.create_frecuencia, name='create_frecuencia'),
    path('update_frecuencia/', views.update_frecuencia, name='update_frecuencia'),
    path('delete_frecuencia/<int:frecuencia_id>', views.delete_frecuencia, name='delete_frecuencia'),

    #   EVENTO
    path('eventos/', views.EventosView, name='eventos'),
    path('evento/<int:event_id>/',views.EventoView, name='evento'),
    path('create_evento/', views.create_evento, name='create_evento'),
    path('update_evento/', views.update_evento, name='update_evento'),
    path('done_evento/<int:evento_id>/', views.done_evento, name='done_evento'),
    path('delete_evento/<int:evento_id>/', views.delete_evento, name='delete_evento'),
    path('verify_evento/', views.verify_evento, name='verify_evento'),

    # TEMAEVENTO
    path('create_temaevento/', views.create_temaevento, name='create_temaevento'),
    path('aprobar_temaevento/', views.aprobar_temaevento, name='aprobar_temaevento'),

    # ACTA
    path('create_acta/', views.create_acta, name='create_acta'),

    # ACUERDO
    path('create_acuerdo/', views.create_acuerdo, name='create_acuerdo'),
]