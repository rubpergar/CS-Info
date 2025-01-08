# encoding:utf-8

import os
import re
import ssl
import time
import urllib.request
from bs4 import BeautifulSoup
from main.models import Region, Rol, Equipo, Jugador

# Configurar contexto SSL para conexiones no verificadas
if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
    ssl._create_unverified_context = ssl._create_unverified_context


def populate():
    """Pobla la base de datos con equipos y jugadores."""
    Region.objects.all().delete()
    Rol.objects.all().delete()
    Equipo.objects.all().delete()
    Jugador.objects.all().delete()

    region_urls = [
        "https://liquipedia.net/counterstrike/Portal:Teams/Europe",
        "https://liquipedia.net/counterstrike/Portal:Teams/CIS",
        "https://liquipedia.net/counterstrike/Portal:Teams/North_America",
        "https://liquipedia.net/counterstrike/Portal:Teams/South_America",
        "https://liquipedia.net/counterstrike/Portal:Teams/Oceania",
        "https://liquipedia.net/counterstrike/Portal:Teams/Asia",
        "https://liquipedia.net/counterstrike/Portal:Teams/Africa",
    ]

    for region_url in region_urls:
        region_name = region_url.split("/")[-1]
        print(f"\nProcesando la región: {region_name}")
        equipos = scrape_region(region_url)

        for equipo_data in equipos:
            equipo = Equipo(nombre=equipo_data["nombre"])
            if not crear_equipo(equipo, equipo_data["link"]):
                print(f"  No se pudo extraer información para el equipo {equipo.nombre}")

    print("\nBase de datos poblada correctamente.")
    return True


def scrape_region(region_url):
    response = urllib.request.urlopen(region_url)
    soup = BeautifulSoup(response, "lxml")
    categorias = ["500,000", "100,000"]
    equipos_dict = {}

    for categoria in categorias:
        equipos_categoria = obtener_equipos_por_categoria(soup, categoria)
        for equipo in equipos_categoria:
            equipos_dict[equipo["nombre"]] = equipo

    return list(equipos_dict.values())


def obtener_equipos_por_categoria(soup, categoria):
    """Obtiene los equipos de una categoría específica."""
    header = soup.find('span', text=re.compile(rf".*{categoria}.*"))
    if not header:
        print(f"  No se encontró la categoría {categoria}")
        return []

    equipos_section = header.find_next("div", class_="toggle-group toggle-state-show")
    if not equipos_section:
        print(f"  No se encontró la sección de equipos para {categoria}")
        return []

    equipos_html = equipos_section.find_all("span", class_="team-template-text")
    equipos = [
        {
            "nombre": equipo_html.text.strip(),
            "link": (equipo_html.find("a")["href"] if equipo_html.find("a") else None)
        }
        for equipo_html in equipos_html if equipo_html.text.strip()
    ]

    return equipos


def crear_equipo(equipo, link):
    try:
        equipo_url = f"https://liquipedia.net{link}"
        time.sleep(2)
        soup = BeautifulSoup(urllib.request.urlopen(equipo_url), "lxml")

        equipo.descripcion = soup.find("div", class_="tabs-static").find_next("p").text.strip() or "Sin descripción"

        region_html = soup.find(string=re.compile("Region:"))
        region_nombre = region_html.find_next().text.strip() if region_html else "Desconocida"
        equipo.region, _ = Region.objects.get_or_create(nombre=region_nombre)

        equipo.entrenador = (
            soup.find(string=re.compile("Coaches:")).find_next("a").find_next("a").text.strip()
            if soup.find(string=re.compile("Coaches:")) else "Desconocido"
        )

        equipo.capitan = (
            soup.find(string=re.compile("In-Game Leader:")).find_next("a").find_next("a").text.strip()
            if soup.find(string=re.compile("In-Game Leader:")) else "Desconocido"
        )

        ganancias_html = soup.find(string=re.compile("Approx. Total Winnings:"))
        equipo.ganancias = (
            float(ganancias_html.find_next().text.strip().replace("$", "").replace(",", ""))
            if ganancias_html and ganancias_html.find_next().text.strip().replace("$", "").replace(",", "").isdigit()
            else 0.0
        )

        equipo.save()

        jugadores_table = soup.find("table", class_="wikitable wikitable-striped roster-card")
        if jugadores_table:
            for jugador_html in jugadores_table.find_all("tr", class_="Player"):
                jugador_nombre = jugador_html.text.strip()
                jugador_link = jugador_html.find_next("a")["href"] if jugador_html.find_next("a") else None
                crear_jugador(jugador_nombre, jugador_link, equipo)

        return True

    except Exception as e:
        print(f"  Error al crear equipo {equipo.nombre}: {e}")
        return False


def crear_jugador(nombre, link, equipo):
    try:
        nick, nombre_real, nacionalidad, roles_nombres = nombre, "Desconocido", "Desconocido", []
        descripcion = "Sin descripción"

        if link:
            jugador_url = f"https://liquipedia.net{link}"
            time.sleep(2)
            soup = BeautifulSoup(urllib.request.urlopen(jugador_url), "lxml")

            overview_html = soup.find("div", class_="tabs-static").find_next("p")
            descripcion = overview_html.text.strip() if overview_html else "Sin descripción"

            nick = soup.find("h1", {"id": "firstHeading"}).text.strip()

            romanized_name_html = soup.find(string=re.compile("Romanized Name:"))
            nombre_real = (romanized_name_html.find_next().text.strip() if romanized_name_html
                           else (soup.find(string=re.compile("Name:")).find_next().text.strip() if soup.find(string=re.compile("Name:")) else "Desconocido"))

            nacionalidad_html = soup.find(string=re.compile("Nationality:"))
            nacionalidad = nacionalidad_html.find_next("a").find_next("a").text.strip() if nacionalidad_html else "Desconocido"

            ganancias_html = soup.find(string=re.compile("Approx. Total Winnings:"))
            ganancias = (
                ganancias_html.find_next().text.strip().replace("$", "").replace(",", "")
                if ganancias_html else "0"
            )

            roles_html = soup.find(string=re.compile(r"Role[s]?:"))
            if roles_html:
                roles_links = roles_html.find_next("div").find_all("a")
                roles_nombres = [role.text.strip() for role in roles_links]

        jugador, created = Jugador.objects.get_or_create(
            nick=nick,
            defaults={
                "nombre_real": nombre_real,
                "nacionalidad": nacionalidad,
                "equipo": equipo,
                "ganancias": float(ganancias) if ganancias.isdigit() else 0.0,
                "descripcion": descripcion,
            }
        )

        for rol_nombre in roles_nombres:
            rol, _ = Rol.objects.get_or_create(nombre=rol_nombre)
            jugador.roles.add(rol)

        jugador.save()
        return True

    except Exception as e:
        print(f"  Error al crear jugador {nombre}: {e}")
        return False
