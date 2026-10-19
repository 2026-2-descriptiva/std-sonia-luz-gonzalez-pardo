def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        4
    """

    raise NotImplementedError

from pathlib import Path
import pandas as pd


def pregunta_02():
    """
    ¿Cuántas columnas tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.
    """
    data_path = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"
    df = pd.read_csv(data_path, sep="\t")
    return len(df.columns)


if __name__ == "__main__":
    print(pregunta_02())