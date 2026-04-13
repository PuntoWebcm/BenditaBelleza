from django.shortcuts import render, get_object_or_404, redirect
from .models import Servicio, Turno, Clienta # <--- Agregamos Clienta aquí

def index(request):
    """Muestra la Landing Page con todos los servicios disponibles"""
    servicios = Servicio.objects.all()
    return render(request, 'index.html', {'servicios': servicios})

def seleccionar_hora(request, servicio_id):
    """Muestra los turnos disponibles (libres) para un servicio específico"""
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    turnos_disponibles = Turno.objects.filter(
        servicio=servicio, 
        disponible=True
    ).order_by('fecha', 'hora')
    
    return render(request, 'calendario.html', {
        'servicio': servicio,
        'turnos': turnos_disponibles
    })

def confirmar_turno(request, turno_id):
    """Procesa la reserva, crea/busca la clienta y abre WhatsApp"""
    turno = get_object_or_404(Turno, pk=turno_id)
    
    if request.method == 'POST':
        nombre_ingresado = request.POST.get('nombre_cliente')
        telefono_ingresado = request.POST.get('telefono_cliente')
        
        # LÓGICA MÁGICA:
        # Buscamos una clienta con ese teléfono. 
        # Si existe, la usamos. Si no existe, la creamos con ese nombre.
        clienta_obj, created = Clienta.objects.get_or_create(
            telefono=telefono_ingresado,
            defaults={'nombre': nombre_ingresado}
        )
        
        # Si la clienta ya existía pero cambió su nombre (ej: puso un apodo), 
        # opcionalmente podrías actualizarlo, pero por ahora la dejamos así.

        # Guardamos la vinculación en el turno
        turno.clienta = clienta_obj # <--- Ahora vinculamos el objeto Clienta
        turno.disponible = False
        turno.save()

        # Armamos el mensaje para WhatsApp
        mensaje = (
            f"¡Hola! Soy *{clienta_obj.nombre}*. "
            f"Acabo de reservar el turno de *{turno.servicio.nombre}* "
            f"para el día {turno.fecha} a las {turno.hora}hs. "
            f"Mi teléfono de contacto es {clienta_obj.telefono}."
        )
        
        mensaje_url = mensaje.replace(' ', '%20')
        url_whatsapp = f"https://wa.me/{turno.servicio.telefono_whatsapp}?text={mensaje_url}"
        
        return redirect(url_whatsapp)
    
    return redirect('index')