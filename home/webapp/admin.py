from django.contrib import admin
from .models import InfraredSignal, Lock

admin.site.register(InfraredSignal)
admin.site.register(Lock)
