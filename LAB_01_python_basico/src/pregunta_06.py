import gzip
from pathlib import Path


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.
    """
    valores_por_clave = {}
    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    with gzip.open(data_path, "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if len(columnas) > 4:
                elementos = columnas[4].strip().split(",")
                for elem in elementos:
                    if ":" in elem:
                        clave, val_str = elem.split(":")
                        clave = clave.strip()
                        val = int(val_str.strip())
                        if clave not in valores_por_clave:
                            valores_por_clave[clave] = []
                        valores_por_clave[clave].append(val)

    resultado = [
        (clave, min(vals), max(vals))
        for clave, vals in sorted(valores_por_clave.items())
    ]
    return resultado


if __name__ == "__main__":
    print(pregunta_06())