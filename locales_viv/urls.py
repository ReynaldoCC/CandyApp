from django.contrib import admin
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
# from django.conf.urls import handler404, handler403, handler500, handler400
# from apps.dpv_base.views import error400, error403, error404, error500
# from apps.dpv_base.views import tesview
from django.conf.urls.static import static
from django.conf import settings

# handler400 = error400
# handler403 = error403
# handler404 = error404
# handler500 = error500


urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
#     path('1234', tesview),
    path('dj-admin/', admin.site.urls),
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

]
