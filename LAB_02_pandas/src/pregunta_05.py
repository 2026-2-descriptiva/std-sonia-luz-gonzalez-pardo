def pregunta_05():
    """
    Usando `data/tbl0.tsv`, encuentre el valor máximo de la columna `c2` para
    cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice
    son las categorías, en orden alfabético, y cuyos valores son los máximos.

    Ejemplo del formato de la respuesta:

        c1
        A    9
        B    9
        C    9
        ...
    """

    raise NotImplementedError

from pathlib import Path
import pandas as pd


def pregunta_05():
    """
    Usando `data/tbl0.tsv`, encuentre el valor máximo de la columna `c2` para
    cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice
    son las categorías, en orden alfabético, y cuyos valores son los máximos.
    """
    data_path = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"
    df = pd.read_csv(data_path, sep="\t")
    return df.groupby("c1")["c2"].max()


if __name__ == "__main__":
    print(pregunta_05())