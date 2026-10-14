def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    raise NotImplementedError
import gzip
from pathlib import Path


def pregunta_03():
    sumas = {}
    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    with gzip.open(data_path, "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if len(columnas) > 1:
                letra = columnas[0].strip()
                try:
                    valor = int(columnas[1].strip())
                    sumas[letra] = sumas.get(letra, 0) + valor
                except ValueError:
                    continue

    return sorted(sumas.items())


if __name__ == "__main__":
    print(pregunta_03())