from django.shortcuts import render, get_object_or_404, redirect
from .models import Servicio, Turno

def index(request):
    """Landing Page"""
    servicios = Servicio.objects.all()
    return render(request, 'index.html', {'servicios': servicios})

def seleccionar_hora(request, servicio_id):
    """Página de calendario/horarios"""
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    turnos_disponibles = Turno.objects.filter(servicio=servicio, disponible=True).order_by('fecha', 'hora')
    
    return render(request, 'calendario.html', {
        'servicio': servicio,
        'turnos': turnos_disponibles
    })

def confirmar_turno(request, turno_id):
    """Redirección a WhatsApp"""
    turno = get_object_or_404(Turno, pk=turno_id)
    
    # Marcamos como no disponible
    turno.disponible = False
    turno.save()

    # Mensaje para WhatsApp
    mensaje = f"Hola! Me gustaría confirmar un turno para *{turno.servicio.nombre}* el día {turno.fecha} a las {turno.hora}."
    url_whatsapp = f"https://wa.me/{turno.servicio.telefono_whatsapp}?text={mensaje.replace(' ', '%20')}"
    
    return redirect(url_whatsapp)
