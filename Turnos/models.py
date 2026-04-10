from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100) # Ej: Manicura
    descripcion = models.TextField()
    telefono_whatsapp = models.CharField(max_length=20) # Ej: 5491122334455
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nombre

class Turno(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='turnos')
    fecha = models.DateField()
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.servicio.nombre} - {self.fecha} a las {self.hora}"
