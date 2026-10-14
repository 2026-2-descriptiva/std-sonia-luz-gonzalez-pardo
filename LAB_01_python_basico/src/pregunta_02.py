def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

    raise NotImplementedError
import gzip


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """
    conteo = {}

    # PASO 1: Abrimos el archivo comprimido
    with gzip.open("data/data.csv.gz", "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if columnas:
                letra = columnas[0].strip()
                # Omitimos si es el encabezado de la columna
                if letra == "letter" or not letra:
                    continue
                # Acumulamos el conteo por cada letra
                conteo[letra] = conteo.get(letra, 0) + 1

    # PASO 2: Convertimos el diccionario a una lista de tuplas y la ordenamos alfabéticamente
    resultado = sorted(conteo.items())

    return resultado