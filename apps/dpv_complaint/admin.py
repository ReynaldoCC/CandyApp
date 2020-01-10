from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Complaint)
admin.site.register(Technical)
admin.site.register(AssignedToTechnician)
admin.site.register(Accepted)
admin.site.register(HistoryComplaint)
