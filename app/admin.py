from django.contrib import admin
from .models import Config,Constraint,Shift,Station

admin.site.register(Config)
admin.site.register(Constraint)
admin.site.register(Shift)
admin.site.register(Station)
