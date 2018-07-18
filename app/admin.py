from django.contrib import admin
from .models import Config,Seq,Station,Shift

admin.site.register(Config)
admin.site.register(Seq)
admin.site.register(Station)
admin.site.register(Shift)
