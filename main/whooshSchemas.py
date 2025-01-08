from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD
from whoosh.index import create_in, open_dir
import os
import shutil
from main.models import Jugador, Equipo


def crear_esquemas():
    jugador_schema = Schema(
        nick=TEXT(stored=True),
        nombre_real=TEXT(stored=True),
        nacionalidad=TEXT(stored=True),
        roles=KEYWORD(stored=True, commas=True),
        ganancias=NUMERIC(stored=True, decimal_places=2),
        descripcion=TEXT(stored=True),
        equipo=TEXT(stored=True),
    )

    equipo_schema = Schema(
        nombre=TEXT(stored=True),
        region=TEXT(stored=True),
        entrenador=TEXT(stored=True),
        capitan=TEXT(stored=True),
        ganancias=NUMERIC(stored=True, decimal_places=2),
        descripcion=TEXT(stored=True),
        jugadores=TEXT(stored=True),
    )

    if os.path.exists("Index_Jugadores"):
        shutil.rmtree("Index_Jugadores")
    os.mkdir("Index_Jugadores")

    if os.path.exists("Index_Equipos"):
        shutil.rmtree("Index_Equipos")
    os.mkdir("Index_Equipos")

    # Crear índices
    create_in("Index_Jugadores", schema=jugador_schema)
    create_in("Index_Equipos", schema=equipo_schema)


def indexar_jugadores():
    try:
        ix = open_dir("Index_Jugadores")
        writer = ix.writer()

        jugadores = Jugador.objects.prefetch_related('roles', 'equipo').all()

        for jugador in jugadores:
            roles = [rol.nombre for rol in jugador.roles.all()]
            writer.add_document(
                nick=jugador.nick,
                nombre_real=jugador.nombre_real or "",
                nacionalidad=jugador.nacionalidad or "",
                roles=",".join(roles),
                ganancias=float(jugador.ganancias),
                descripcion=jugador.descripcion or "",
                equipo=jugador.equipo.nombre if jugador.equipo else "",
            )

        writer.commit(optimize=True)
        print("Indexación de jugadores completada.")
    except Exception as e:
        print(f"Error al indexar jugadores: {e}")


def indexar_equipos():
    try:
        ix = open_dir("Index_Equipos")
        writer = ix.writer()

        equipos = Equipo.objects.prefetch_related('jugador_set', 'region').all()

        for equipo in equipos:
            jugadores = ", ".join([jugador.nick for jugador in equipo.jugador_set.all()])
            writer.add_document(
                nombre=equipo.nombre,
                region=equipo.region.nombre,
                entrenador=equipo.entrenador or "",
                capitan=equipo.capitan or "",
                ganancias=float(equipo.ganancias),
                descripcion=equipo.descripcion or "",
                jugadores=jugadores,
            )

        writer.commit(optimize=True)
        print("Indexación de equipos completada.")
    except Exception as e:
        print(f"Error al indexar equipos: {e}")


def inicializar_indices():
    print("\nCreando esquemas e índices...")
    crear_esquemas()
    print("Esquemas creados. Indexando datos...")
    indexar_jugadores()
    indexar_equipos()
    print("Indexación completada.\n")
