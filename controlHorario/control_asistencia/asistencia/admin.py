# admin.py
from django.contrib import admin
from .models import Trabajador, Asistencia, Admin

admin.site.register(Trabajador)
admin.site.register(Asistencia)
admin.site.register(Admin)
