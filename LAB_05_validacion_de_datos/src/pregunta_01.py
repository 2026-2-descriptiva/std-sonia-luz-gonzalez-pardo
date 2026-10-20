def main():
    """
    Antes de limpiar o analizar un conjunto de datos, un analista debe
    documentar qué problemas tiene. En este laboratorio usted no va a limpiar
    `data/ventas.csv.gz`: va a construir un reporte de calidad que deje evidencia
    de sus problemas, tal como están en el archivo.

    Lea `data/ventas.csv.gz` sin modificar sus valores. Para trabajar con los
    encabezados, normalícelos: páselos a minúsculas, elimine los espacios al
    inicio y al final (y cualquier marca BOM) y reemplace los espacios
    internos por `_`. Las columnas requeridas son `supplier_id`, `supplier`,
    `country`, `city`, `purchase_date`, `amount`, `discount`, `weight`,
    `units`, `unit_price` y `contact_email`.

    Escriba el reporte en `submission/data_quality_report.json` con estas
    claves:

    - `row_count`: cantidad de filas de datos.
    - `column_count`: cantidad de columnas.
    - `missing_required_columns`: lista ordenada de columnas requeridas que no
      están en el archivo.
    - `unexpected_columns`: lista ordenada de columnas del archivo que no son
      requeridas.
    - `duplicate_row_count`: cantidad de filas idénticas a una fila anterior.
    - `duplicate_supplier_id_row_count`: cantidad de filas cuyo `supplier_id`
      aparece más de una vez (cuente todas esas filas, no solo las
      repetidas).
    - `missing_value_count_by_column`: diccionario con la cantidad de valores
      faltantes de cada columna. Considere faltantes las celdas vacías y las
      que contienen `N/A`.
    - `invalid_email_count`: cantidad de valores de `contact_email` que no
      tienen la forma `usuario@dominio.extension`.
    - `invalid_unit_count`: cantidad de valores numéricos de `units` que no son
      enteros positivos. Los valores faltantes no se cuentan aquí.
    - `country_values`: lista ordenada de los valores distintos de `country`,
      escritos exactamente como aparecen en el archivo.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "row_count": 103,
          "column_count": 11,
          "missing_required_columns": [],
          ...
          "country_values": [" Colombia ", "CO", ...]
        }
    """

    raise NotImplementedError

import gzip
import json
import re
from pathlib import Path
import pandas as pd


def main():
    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "ventas.csv.gz"
    submission_dir = base_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    # 1. Leer CSV sin modificar valores, tratando cadenas vacías y "N/A"
    # Leemos todo como string para evitar conversiones automáticas imprevistas
    df = pd.read_csv(data_path, compression="gzip", dtype=str, keep_default_na=False)

    # Normalizar encabezados: minúsculas, strip, eliminar BOM y espacios por '_'
    def normalizar_columna(col):
        col_clean = str(col).replace("\ufeff", "").strip().lower()
        return re.sub(r"\s+", "_", col_clean)

    df.columns = [normalizar_columna(c) for c in df.columns]

    required_columns = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email",
    ]

    # Métricas básicas
    row_count = len(df)
    column_count = len(df.columns)

    missing_required = sorted(list(set(required_columns) - set(df.columns)))
    unexpected = sorted(list(set(df.columns) - set(required_columns)))

    # Filas duplicadas idénticas
    duplicate_row_count = int(df.duplicated(keep="first").sum())

    # Filas cuyo supplier_id aparece más de una vez
    if "supplier_id" in df.columns:
        counts = df["supplier_id"].value_counts()
        repetidos = counts[counts > 1]
        duplicate_supplier_id_row_count = int(repetidos.sum())
    else:
        duplicate_supplier_id_row_count = 0

    # Conteo de faltantes (vacíos o "N/A") por columna
    missing_value_count_by_column = {}
    for col in df.columns:
        is_missing = df[col].astype(str).isin(["", "N/A", "nan", "None"])
        missing_value_count_by_column[col] = int(is_missing.sum())

    # Correos inválidos en contact_email
    email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    invalid_email_count = 0
    if "contact_email" in df.columns:
        for val in df["contact_email"]:
            val_str = str(val).strip()
            if val_str not in ["", "N/A", "nan", "None"]:
                if not email_regex.match(val_str):
                    invalid_email_count += 1

    # Unidades inválidas en units (no enteros positivos, omitiendo faltantes)
    invalid_unit_count = 0
    if "units" in df.columns:
        for val in df["units"]:
            val_str = str(val).strip()
            if val_str not in ["", "N/A", "nan", "None"]:
                try:
                    num = float(val_str)
                    if not (num.is_integer() and num > 0):
                        invalid_unit_count += 1
                except ValueError:
                    invalid_unit_count += 1

    # Valores distintos de country ordenados
    if "country" in df.columns:
        country_values = sorted(list(df["country"].unique()))
    else:
        country_values = []

    # Construir reporte
    report = {
        "row_count": row_count,
        "column_count": column_count,
        "missing_required_columns": missing_required,
        "unexpected_columns": unexpected,
        "duplicate_row_count": duplicate_row_count,
        "duplicate_supplier_id_row_count": duplicate_supplier_id_row_count,
        "missing_value_count_by_column": missing_value_count_by_column,
        "invalid_email_count": invalid_email_count,
        "invalid_unit_count": invalid_unit_count,
        "country_values": country_values,
    }

    # Guardar en archivo JSON
    report_file = submission_dir / "data_quality_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    return report


if __name__ == "__main__":
    print(main())
