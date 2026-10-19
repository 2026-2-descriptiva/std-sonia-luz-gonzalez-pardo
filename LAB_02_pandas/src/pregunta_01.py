def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """

    raise NotImplementedError

from pathlib import Path
import pandas as pd


def pregunta_01():
    # 1. Encontrar la ruta del archivo
    data_path = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # 2. Cargar el archivo con pandas
    df = pd.read_csv(data_path, sep="\t")

    # 3. Contar los registros
    return len(df)