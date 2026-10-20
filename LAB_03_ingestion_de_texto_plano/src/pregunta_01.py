def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    raise NotImplementedError

import re
from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    Convierte el reporte `clusters_report.txt` en un DataFrame de Pandas estructurado.
    """
    data_path = Path(__file__).resolve().parents[1] / "data" / "clusters_report.txt"

    clusters = []
    cluster_actual = None

    with open(data_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines[4:]:
        if not line.strip():
            continue

        match = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)", line)

        if match:
            if cluster_actual:
                # Unir lineas y normalizar espacios internos
                texto_completo = " ".join(cluster_actual["palabras"])
                texto_limpio = re.sub(r"\s+", " ", texto_completo)
                
                # Separar por comas, quitar espacios laterales y eliminar punto final
                palabras = [p.strip() for p in texto_limpio.split(",") if p.strip()]
                palabras_unidas = ", ".join(palabras)
                if palabras_unidas.endswith("."):
                    palabras_unidas = palabras_unidas[:-1]

                clusters.append({
                    "cluster": cluster_actual["cluster"],
                    "cantidad_de_palabras_clave": cluster_actual["cantidad"],
                    "porcentaje_de_palabras_clave": cluster_actual["porcentaje"],
                    "principales_palabras_clave": palabras_unidas,
                })

            cluster_num = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(",", "."))
            palabras_iniciales = match.group(4).strip()

            cluster_actual = {
                "cluster": cluster_num,
                "cantidad": cantidad,
                "porcentaje": porcentaje,
                "palabras": [palabras_iniciales],
            }
        else:
            if cluster_actual:
                cluster_actual["palabras"].append(line.strip())

    # Procesar el último clúster
    if cluster_actual:
        texto_completo = " ".join(cluster_actual["palabras"])
        texto_limpio = re.sub(r"\s+", " ", texto_completo)
        palabras = [p.strip() for p in texto_limpio.split(",") if p.strip()]
        palabras_unidas = ", ".join(palabras)
        if palabras_unidas.endswith("."):
            palabras_unidas = palabras_unidas[:-1]

        clusters.append({
            "cluster": cluster_actual["cluster"],
            "cantidad_de_palabras_clave": cluster_actual["cantidad"],
            "porcentaje_de_palabras_clave": cluster_actual["porcentaje"],
            "principales_palabras_clave": palabras_unidas,
        })

    return pd.DataFrame(clusters)


if __name__ == "__main__":
    print(pregunta_01())