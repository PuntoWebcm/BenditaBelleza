from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    telefono_whatsapp = models.CharField(max_length=20)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nombre

class Clienta(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono/WhatsApp")

    class Meta:
        verbose_name = "Clienta"
        verbose_name_plural = "Clientas"

    def __str__(self):
        return self.nombre

class Turno(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='turnos')
    fecha = models.DateField()
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)
    
    clienta = models.ForeignKey(Clienta, on_delete=models.SET_NULL, blank=True, null=True, related_name='historial')
    
    notas_tecnicas = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Notas del servicio",
        help_text="Ej: Tintura 7.1, Mechas con gorra, Alisado fuerte, etc."
    )

    # --- NUEVOS CAMPOS DE DINERO ---
    precio_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="Precio del Trabajo ($)"
    )
    pagado_hasta_ahora = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="Monto ya pagado ($)"
    )

    # Función para calcular la deuda de ESTE turno específico
    def deuda_pendiente(self):
        return self.precio_total - self.pagado_hasta_ahora

    def __str__(self):
        if not self.disponible and self.clienta:
            return f"RESERVADO: {self.clienta.nombre} - {self.fecha} a las {self.hora}"
        return f"Libre: {self.fecha} a las {self.hora}"