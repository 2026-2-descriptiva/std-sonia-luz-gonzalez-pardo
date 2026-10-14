import gzip
import os


def pregunta_01():
    """
    Calcule la suma de los valores de la segunda columna (`value`) del
    archivo `data/data.csv.gz` y retorne el resultado como un número entero.
    """
    suma_total = 0

    # Construimos la ruta dinámica hacia data/data.csv.gz
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "data.csv.gz")

    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if len(columnas) > 1:
                try:
                    suma_total += int(columnas[1])
                except ValueError:
                    continue

    return suma_total


if __name__ == "__main__":
    print(pregunta_01())