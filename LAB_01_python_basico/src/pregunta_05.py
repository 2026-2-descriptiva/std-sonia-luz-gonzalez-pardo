def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    raise NotImplementedError
import gzip
from pathlib import Path


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.
    """
    valores_por_letra = {}
    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    with gzip.open(data_path, "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if len(columnas) > 1:
                letra = columnas[0].strip()
                try:
                    val = int(columnas[1].strip())
                    if letra not in valores_por_letra:
                        valores_por_letra[letra] = []
                    valores_por_letra[letra].append(val)
                except ValueError:
                    continue

    resultado = [
        (letra, max(vals), min(vals))
        for letra, vals in sorted(valores_por_letra.items())
    ]
    return resultado


if __name__ == "__main__":
    print(pregunta_05())