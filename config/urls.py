"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Turnos.urls')),
]

# Configuración para servir archivos estáticos (imágenes, CSS) en producción
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

   # --- ULTIMO INTENTO DE ADMIN ---
from django.contrib.auth.models import User
try:
    # Si ya existe, lo borramos para resetear la clave
    u = User.objects.filter(username='admin').first()
    if u:
        u.delete()
    
    # Lo creamos de cero con permisos totales
    new_user = User.objects.create_superuser('admin', 'admin@bendita.com', 'admin12345')
    new_user.is_staff = True
    new_user.is_superuser = True
    new_user.save()
    print("---------------------------------------")
    print("¡USUARIO RE-CREADO: admin / admin12345!")
    print("---------------------------------------")
except Exception as e:
    print(f"Error: {e}")