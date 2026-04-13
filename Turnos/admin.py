from django.contrib import admin
from .models import Servicio, Turno, Clienta
from django.utils import timezone

# Títulos personalizados
admin.site.site_header = "Panel de Gestión - Bendita Belleza"
admin.site.index_title = "Agenda de Reservas"
admin.site.site_title = "Bendita Belleza"

# --- CONFIGURACIÓN PARA EL HISTORIAL DENTRO DE LA CLIENTA ---
class HistorialTurnosInline(admin.TabularInline):
    model = Turno
    extra = 0
    # Agregamos los campos de dinero al historial para que se vea cuánto pagó en cada visita
    fields = ('fecha', 'hora', 'servicio', 'precio_total', 'pagado_hasta_ahora', 'notas_tecnicas')
    readonly_fields = ('fecha', 'hora', 'servicio')
    can_delete = False
    verbose_name = "Turno Pasado"
    verbose_name_plural = "Historial de Visitas"

@admin.register(Clienta)
class ClientaAdmin(admin.ModelAdmin):
    # Agregamos la columna 'deuda_total' a la lista de clientas
    list_display = ('nombre', 'telefono', 'deuda_total')
    search_fields = ('nombre', 'telefono')
    inlines = [HistorialTurnosInline]

    def deuda_total(self, obj):
        # Sumamos la diferencia de todos sus turnos
        total = sum(t.deuda_pendiente() for t in obj.historial.all())
        if total > 0:
            return f"⚠️ DEBE ${total}"
        return "✅ Al día"
    deuda_total.short_description = 'Saldo Deudor'

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono_whatsapp', 'precio')

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    # Agregamos 'get_deuda' para ver el saldo de cada turno en la tabla principal
    list_display = ('fecha', 'hora', 'get_nombre_cliente', 'servicio', 'precio_total', 'get_deuda', 'estado_temporal', 'estado_reserva')
    list_filter = ('disponible', 'fecha', 'servicio')
    search_fields = ('clienta__nombre', 'clienta__telefono')
    ordering = ('fecha', 'hora')

    def get_deuda(self, obj):
        deuda = obj.deuda_pendiente()
        if deuda > 0:
            return f"❌ Debe ${deuda}"
        return "✅ Pagado"
    get_deuda.short_description = 'Saldo'

    def estado_temporal(self, obj):
        hoy = timezone.now().date()
        if obj.fecha < hoy:
            return "⏳ Pasado"
        elif obj.fecha == hoy:
            return "⭐ Hoy"
        return "📅 Próximo"
    estado_temporal.short_description = 'Vigencia'

    def get_nombre_cliente(self, obj):
        return obj.clienta.nombre if obj.clienta else "N/A"
    get_nombre_cliente.short_description = 'Clienta'

    def estado_reserva(self, obj):
        if not obj.disponible:
            return "✅ Reservado"
        return "❌ Libre"
    estado_reserva.short_description = 'Estado'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        hoy = timezone.now().date()
        if not request.GET:
            return qs.filter(disponible=False, fecha__gte=hoy)
        return qs