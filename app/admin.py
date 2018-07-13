from django.contrib import admin
from .models import Constraint,Config,Seq,Station,Shift

admin.site.register(Constraint)
admin.site.register(Config)
admin.site.register(Seq)
admin.site.register(Station)
admin.site.register(Shift)
