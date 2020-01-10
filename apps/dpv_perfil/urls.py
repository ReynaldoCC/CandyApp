from django.urls import path
from .views import index
from apps.dpv_base.views import change_pass

urlpatterns = [
    path('', index, name='perfil_detail'),
    path('passwd/', change_pass, name='perfil_changepass')
]