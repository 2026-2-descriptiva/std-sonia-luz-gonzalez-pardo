import gzip
from pathlib import Path


def pregunta_04():
    """
    Cuente cuántos registros hay en cada mes, usando la fecha de la tercera
    columna (`date`). Represente el mes como un texto de dos dígitos y retorne
    una lista de tuplas `(mes, cantidad)` ordenada por el mes.
    """
    conteo_mes = {}
    data_path = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    with gzip.open(data_path, "rt", encoding="utf-8") as f:
        for linea in f:
            columnas = linea.strip().split("\t")
            if len(columnas) > 2:
                fecha = columnas[2].strip()
                partes = fecha.split("-")
                if len(partes) == 3:
                    mes = partes[1]
                    conteo_mes[mes] = conteo_mes.get(mes, 0) + 1

    return sorted(conteo_mes.items())


