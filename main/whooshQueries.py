from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import NumericRange


def buscar_jugadores(consulta, campos=None):
    campos = campos or ["nick", "nombre_real", "descripcion"]
    resultados = []

    try:
        ix = open_dir("Index_Jugadores")
        with ix.searcher() as searcher:
            parser = MultifieldParser(campos, schema=ix.schema)
            query = parser.parse(consulta)
            results = searcher.search(query)

            for result in results:
                resultados.append(dict(result))
    except Exception as e:
        print(f"Error en la búsqueda de jugadores: {e}")

    return resultados


def buscar_equipos(consulta, campos=None):
    campos = campos or ["nombre", "descripcion"]
    resultados = []

    try:
        ix = open_dir("Index_Equipos")
        with ix.searcher() as searcher:
            parser = MultifieldParser(campos, schema=ix.schema)
            query = parser.parse(consulta)
            results = searcher.search(query, limit=20)

            for result in results:
                resultados.append(dict(result))
    except Exception as e:
        print(f"Error en la búsqueda de equipos: {e}")

    return resultados


def buscar_equipos_por_descripcion_y_region(descripcion, region):
    resultados = []

    try:
        ix = open_dir("Index_Equipos")
        with ix.searcher() as searcher:
            query = f"descripcion:{descripcion} AND region:{region}"
            parser = QueryParser("descripcion", schema=ix.schema)
            query = parser.parse(query)
            results = searcher.search(query, limit=20)

            for result in results:
                resultados.append(dict(result))
    except Exception as e:
        print(f"Error en la búsqueda de equipos por descripción y región: {e}")

    return resultados


def buscar_jugadores_por_rango_ganancias(min_ganancias, max_ganancias):
    ix = open_dir("Index_Jugadores")
    with ix.searcher() as searcher:
        query = NumericRange("ganancias", min_ganancias, max_ganancias)
        results = searcher.search(query, limit=None)

        resultados = [dict(r) for r in results]

        resultados_ordenados = sorted(resultados, key=lambda x: x["ganancias"], reverse=True)

        return resultados_ordenados
