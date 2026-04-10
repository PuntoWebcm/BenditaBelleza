from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('servicio/<int:servicio_id>/', views.seleccionar_hora, name='seleccionar_hora'),
    path('confirmar/<int:turno_id>/', views.confirmar_turno, name='confirmar_turno'),
]