def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    raise NotImplementedError

import gzip
from pathlib import Path


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.
    """
    resultado = {}
    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    with gzip.open(data_path, "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if len(columnas) > 4:
                letra = columnas[0].strip()
                suma_fila = 0
                elementos = columnas[4].strip().split(",")
                for elem in elementos:
                    if ":" in elem:
                        try:
                            valor = int(elem.split(":")[1].strip())
                            suma_fila += valor
                        except ValueError:
                            continue
                resultado[letra] = resultado.get(letra, 0) + suma_fila

    return dict(sorted(resultado.items()))


if __name__ == "__main__":
    print(pregunta_12())