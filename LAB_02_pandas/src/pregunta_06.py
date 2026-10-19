def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    raise NotImplementedError

from pathlib import Path
import pandas as pd


def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.
    """
    # 1. Buscar el archivo en la despensa
    data_path = Path(__file__).resolve().parents[1] / "data" / "tbl1.tsv"

    # 2. Leer la tabla de datos
    df = pd.read_csv(data_path, sep="\t")

    # 3. Filtrar únicos, convertir a mayúsculas y ordenar
    valores_mayus = df["c4"].str.upper().unique()
    return sorted(list(valores_mayus))


if __name__ == "__main__":
    print(pregunta_06())