from django.urls import path, include
from apps.dpv_base import urls as base_url
from apps.dpv_nomencladores import urls as nomencladores_url
from apps.dpv_locales import urls as locales_url
from apps.dpv_persona import urls as persona_url
from apps.dpv_perfil import urls as perfil_url
from apps.dpv_viviendas import urls as vivienda_url
from apps.dpv_events import urls as events_url
from apps.email_sender import urls as email_url
from apps.dpv_quejas import urls as quejas_url
from apps.dpv_respuesta import urls as respuestas_url
from apps.dpv_documento import urls as docs_url
from apps.dpv_notificaciones import urls as notifies_url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('', include(base_url)),
    path('nomenclador/', include(nomencladores_url)),
    path('local/', include(locales_url)),
    path('persona/', include(persona_url)),
    path('quejas/', include(quejas_url)),
    path('perfil/', include(perfil_url)),
    path('vivienda/', include(vivienda_url)),
    path('dpv_events/', include(events_url)),
    path('emailing/', include(email_url)),
    path('respuesta/', include(respuestas_url)),
    path('docs/', include(docs_url)),
    path('notifies/', include(notifies_url)),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
