def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    raise NotImplementedError

import gzip
from pathlib import Path


def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.
    """
    sumas = {}
    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    with gzip.open(data_path, "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if len(columnas) > 3:
                try:
                    valor = int(columnas[1].strip())
                    letras = columnas[3].strip().split(",")
                    for letra in letras:
                        l = letra.strip()
                        if l:
                            sumas[l] = sumas.get(l, 0) + valor
                except ValueError:
                    continue

    return dict(sorted(sumas.items()))


if __name__ == "__main__":
    print(pregunta_11())