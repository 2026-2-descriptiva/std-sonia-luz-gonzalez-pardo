import gzip
from pathlib import Path


def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.
    """
    letras_por_valor = {}
    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    with gzip.open(data_path, "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if len(columnas) > 1:
                letra = columnas[0].strip()
                try:
                    valor = int(columnas[1].strip())
                    if valor not in letras_por_valor:
                        letras_por_valor[valor] = []
                    letras_por_valor[valor].append(letra)
                except ValueError:
                    continue

    return sorted(letras_por_valor.items())


if __name__ == "__main__":
    print(pregunta_07())