from django.contrib import admin
from .models import PersonaNatural, PersonaJuridica

# Register your models here.
admin.site.register(PersonaNatural)
admin.site.register(PersonaJuridica)
