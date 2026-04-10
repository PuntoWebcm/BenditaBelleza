from django.contrib import admin
from .models import Servicio, Turno

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono_whatsapp', 'precio')

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'fecha', 'hora', 'disponible')
    list_filter = ('servicio', 'fecha', 'disponible')
    list_editable = ('disponible',) # Para marcar ocupado rápido desde la lista