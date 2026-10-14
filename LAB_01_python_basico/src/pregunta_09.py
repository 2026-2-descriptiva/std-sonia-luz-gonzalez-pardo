def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    raise NotImplementedError

import gzip
from pathlib import Path


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.
    """
    conteo_claves = {}
    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    with gzip.open(data_path, "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if len(columnas) > 4:
                elementos = columnas[4].strip().split(",")
                for elem in elementos:
                    if ":" in elem:
                        clave = elem.split(":")[0].strip()
                        conteo_claves[clave] = conteo_claves.get(clave, 0) + 1

    return dict(sorted(conteo_claves.items()))


if __name__ == "__main__":
    print(pregunta_09())