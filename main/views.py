# encoding:utf-8

from main.models import Equipo, Jugador, Region
from main.populateDB import populate
from django.shortcuts import render, get_object_or_404
from .whooshQueries import (
    buscar_equipos_por_descripcion_y_region,
    buscar_jugadores_por_rango_ganancias,
)
from .whooshSchemas import inicializar_indices


def populateDatabase(request):
    """
    Poblar la base de datos y crear índices de búsqueda.
    """
    result = populate()
    if result:
        try:
            inicializar_indices()
            informacion = "Base de datos poblada e índices creados correctamente."
        except Exception as e:
            informacion = f"Base de datos poblada, pero hubo un error al crear los índices: {e}"
    else:
        informacion = "Hubo un error al poblar la base de datos."

    return render(request, 'carga.html', {'inf': informacion})


def listar(request):
    regiones = Region.objects.all()
    equipos = Equipo.objects.all()
    jugadores = Jugador.objects.all()

    contexto = {
        'regiones': regiones,
        'equipos': equipos,
        'jugadores': jugadores,
    }

    return render(request, 'listar.html', contexto)


def buscar(request):
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', 'jugadores')
    resultados = []

    if query:
        if tipo == 'jugadores':
            resultados = (
                Jugador.objects.filter(nick__icontains=query)
                .select_related('equipo')
                .prefetch_related('roles')
            )
        elif tipo == 'equipos':
            equipos = Equipo.objects.select_related('region').prefetch_related('jugador_set')
            resultados = [
                {
                    "equipo": equipo,
                    "jugadores": equipo.jugador_set.all(),
                }
                for equipo in equipos.filter(nombre__icontains=query)
            ]

    return render(request, 'buscar.html', {
        'query': query,
        'tipo': tipo,
        'resultados': resultados,
    })


def buscar_equipos_avanzado(request):
    descripcion = request.GET.get("descripcion", "")
    region = request.GET.get("region", "")
    resultados = buscar_equipos_por_descripcion_y_region(descripcion, region)
    return render(request, "buscar_equipos_avanzado.html", {
        "resultados": resultados,
        "query": f"Descripción: {descripcion}, Región: {region}"
    })


def buscar_jugadores_por_rango(request):
    min_ganancias = request.GET.get("min_ganancias", "0")
    max_ganancias = request.GET.get("max_ganancias", "99999999")

    try:
        resultados = buscar_jugadores_por_rango_ganancias(float(min_ganancias), float(max_ganancias))
    except ValueError:
        resultados = []

    return render(request, "buscar_jugadores_rango_ganancias.html", {
        "resultados": resultados,
        "min_ganancias": min_ganancias,
        "max_ganancias": max_ganancias,
    })


def detalle_jugador(request, idJugador):
    jugador = get_object_or_404(Jugador, idJugador=idJugador)
    return render(request, 'detalle_jugador.html', {
        'jugador': jugador,
    })


def detalle_equipo(request, idEquipo):
    equipo = get_object_or_404(Equipo, idEquipo=idEquipo)
    jugadores = equipo.jugador_set.all()
    return render(request, 'detalle_equipo.html', {
        'equipo': equipo,
        'jugadores': jugadores,
    })


def index(request):
    return render(request, 'index.html')
