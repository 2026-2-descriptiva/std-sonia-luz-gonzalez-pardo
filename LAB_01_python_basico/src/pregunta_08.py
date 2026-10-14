def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    raise NotImplementedError
import gzip
from pathlib import Path


def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.
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
                        letras_por_valor[valor] = set()
                    letras_por_valor[valor].add(letra)
                except ValueError:
                    continue

    resultado = [
        (valor, sorted(list(letras)))
        for valor, letras in sorted(letras_por_valor.items())
    ]
    return resultado


if __name__ == "__main__":
    print(pregunta_08())