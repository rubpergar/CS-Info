from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.index),
    path('populate/', views.populateDatabase),
    path('listar/', views.listar, name='listar'),
    path('buscar/', views.buscar, name="buscar"),
    path('buscar/equipos/avanzado/', views.buscar_equipos_avanzado, name='buscar_equipos_avanzado'),
    path('buscar/jugador/ganancias/', views.buscar_jugadores_por_rango, name='buscar_jugadores_por_rango'),
    path('jugador/<int:idJugador>/', views.detalle_jugador, name='detalle_jugador'),
    path('equipo/<int:idEquipo>/', views.detalle_equipo, name='detalle_equipo'),
    path('admin/', admin.site.urls),
    ]
