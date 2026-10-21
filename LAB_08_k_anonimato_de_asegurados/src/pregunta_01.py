def pregunta_01():
    """
    Una aseguradora quiere publicar datos de sus afiliados para que un grupo
    de investigación estudie el costo de los seguros, sin que nadie pueda
    reconocer a una persona. El archivo `data/insurance.csv.gz` tiene una fila
    por afiliado con su edad (`age`), sexo (`sex`), índice de masa corporal
    (`bmi`), número de hijos (`children`), si fuma (`smoker`), región
    (`region`) y el costo de su seguro (`charges`).

    El archivo no tiene nombres ni documentos, pero eso no basta: la edad, el
    sexo, el índice de masa corporal, el número de hijos y la región son
    cuasi-identificadores, porque combinados pueden señalar a una persona.
    `smoker` es el atributo sensible que se quiere proteger.

    En este laboratorio usted va a medir el riesgo de reidentificación y a
    decidir qué publicar. Use estas definiciones:

    - Una clase de equivalencia es un grupo de registros con los mismos
      valores en todos los cuasi-identificadores. Un conjunto de datos cumple
      k-anonimato si toda clase tiene al menos k registros. Use k = 5.
    - `age_group`: `18-29`, `30-39`, `40-49` o `50-64`.
    - `bmi_group`: `bajo peso` (menos de 18.5), `normal` (desde 18.5 y menos
      de 25), `sobrepeso` (desde 25 y menos de 30) u `obesidad` (30 o más).
    - `children_group`: `0`, `1-2` o `3+`.

    Evalúe dos esquemas de generalización:

    - `with_children`: `age_group`, `sex`, `bmi_group`, `children_group` y
      `region`.
    - `without_children`: `age_group`, `sex`, `bmi_group` y `region`; el
      número de hijos no se publica.

    En cada esquema, suprima (no publique) los registros de las clases con
    menos de 5 registros. Luego, entre las clases publicadas, identifique las
    que no tienen diversidad en el atributo sensible, es decir, aquellas en
    las que todos los afiliados fuman o ninguno fuma: en esas clases, saber
    que alguien pertenece a ellas revela si fuma.

    Escriba `submission/privacy_report.json` con estas claves:

    - `original_k`: el menor tamaño de clase usando los cuasi-identificadores
      originales, sin generalizar.
    - `original_unique_records`: cuántos registros son los únicos de su clase
      con los cuasi-identificadores originales.
    - `schemes`: un diccionario con una entrada por esquema (`with_children` y
      `without_children`), cada una con las claves `quasi_identifiers` (la
      lista de columnas del esquema), `equivalence_classes` (clases antes de
      suprimir), `k_before_suppression`, `suppressed_records`,
      `published_records`, `published_classes`,
      `classes_without_smoker_diversity` y
      `records_without_smoker_diversity`.
    - `selected_scheme`: el esquema que suprime menos registros.
    - `mean_charges_original` y `mean_charges_published`: el costo promedio
      de todos los afiliados y el de los registros publicados con el esquema
      seleccionado.
    - `smoker_rate_original` y `smoker_rate_published`: la proporción de
      fumadores en ambos casos.

    Escriba también `submission/insurance_published.csv`, sin el índice de
    Pandas, con los registros publicados del esquema seleccionado, en el
    mismo orden del archivo original, y las columnas del esquema seguidas de
    `smoker` y `charges`.

    La función también debe retornar el reporte como un diccionario.

    Ejemplo del formato del reporte:

        {
          "original_k": 1,
          "original_unique_records": 1330,
          "schemes": {
            "with_children": {
              "quasi_identifiers": ["age_group", "sex", ...],
              "equivalence_classes": 278,
              ...
            },
            ...
          },
          ...
        }
    """

    raise NotImplementedError


import json
from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    Evalúa esquemas de generalización y k-anonimato (k=5) sobre insurance.csv.gz,
    genera `submission/privacy_report.json` e `submission/insurance_published.csv`.
    """
    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "insurance.csv.gz"
    submission_dir = base_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path, compression="gzip")

    # 1. Análisis sin generalizar (Cuasi-identificadores originales)
    orig_qi = ["age", "sex", "bmi", "children", "region"]
    orig_counts = df.groupby(orig_qi).size()
    original_k = int(orig_counts.min())
    original_unique_records = int((orig_counts == 1).sum())

    # 2. Generalización de columnas
    def get_age_group(age):
        if age <= 29:
            return "18-29"
        elif age <= 39:
            return "30-39"
        elif age <= 49:
            return "40-49"
        else:
            return "50-64"

    def get_bmi_group(bmi):
        if bmi < 18.5:
            return "bajo peso"
        elif bmi < 25.0:
            return "normal"
        elif bmi < 30.0:
            return "sobrepeso"
        else:
            return "obesidad"

    def get_children_group(c):
        if c == 0:
            return "0"
        elif c in [1, 2]:
            return "1-2"
        else:
            return "3+"

    df["age_group"] = df["age"].apply(get_age_group)
    df["bmi_group"] = df["bmi"].apply(get_bmi_group)
    df["children_group"] = df["children"].apply(get_children_group)

    # 3. Definición de Esquemas
    schemes_def = {
        "with_children": ["age_group", "sex", "bmi_group", "children_group", "region"],
        "without_children": ["age_group", "sex", "bmi_group", "region"],
    }

    schemes_report = {}
    published_dfs = {}

    for scheme_name, qi_cols in schemes_def.items():
        # Agrupar para analizar clases de equivalencia antes de suprimir
        counts = df.groupby(qi_cols).size()
        equivalence_classes = len(counts)
        k_before_suppression = int(counts.min())

        # Identificar registros que cumplen k >= 5
        class_sizes = df.groupby(qi_cols)[qi_cols[0]].transform("count")
        mask_k5 = class_sizes >= 5

        suppressed_records = int((~mask_k5).sum())
        published_records = int(mask_k5.sum())

        df_pub = df[mask_k5].copy()
        published_classes = len(df_pub.groupby(qi_cols))

        # Diversidad del atributo sensible (smoker)
        # Clases sin diversidad: todos fuman o ninguno fuma (nunique == 1)
        smoker_diversity = df_pub.groupby(qi_cols)["smoker"].nunique()
        classes_without_smoker_diversity = int((smoker_diversity == 1).sum())

        # Constrastamos con cada fila publicada
        pub_smoker_div = df_pub.groupby(qi_cols)["smoker"].transform("nunique")
        records_without_smoker_diversity = int((pub_smoker_div == 1).sum())

        schemes_report[scheme_name] = {
            "quasi_identifiers": qi_cols,
            "equivalence_classes": equivalence_classes,
            "k_before_suppression": k_before_suppression,
            "suppressed_records": suppressed_records,
            "published_records": published_records,
            "published_classes": published_classes,
            "classes_without_smoker_diversity": classes_without_smoker_diversity,
            "records_without_smoker_diversity": records_without_smoker_diversity,
        }

        published_dfs[scheme_name] = df_pub

    # 4. Selección del Esquema que suprime menos registros
    if (
        schemes_report["with_children"]["suppressed_records"]
        <= schemes_report["without_children"]["suppressed_records"]
    ):
        selected_scheme = "with_children"
    else:
        selected_scheme = "without_children"

    selected_df = published_dfs[selected_scheme]
    selected_qi = schemes_def[selected_scheme]

    # Métricas de impacto/utilidad
    mean_charges_original = float(df["charges"].mean())
    mean_charges_published = float(selected_df["charges"].mean())

    smoker_rate_original = float((df["smoker"] == "yes").mean())
    smoker_rate_published = float((selected_df["smoker"] == "yes").mean())

    # 5. Generar Reporte JSON
    report = {
        "original_k": original_k,
        "original_unique_records": original_unique_records,
        "schemes": schemes_report,
        "selected_scheme": selected_scheme,
        "mean_charges_original": mean_charges_original,
        "mean_charges_published": mean_charges_published,
        "smoker_rate_original": smoker_rate_original,
        "smoker_rate_published": smoker_rate_published,
    }

    with open(submission_dir / "privacy_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    # 6. Guardar CSV publicado (mismo orden del archivo original, columnas QI + smoker + charges)
    cols_to_export = selected_qi + ["smoker", "charges"]
    export_df = selected_df[cols_to_export]
    export_df.to_csv(submission_dir / "insurance_published.csv", index=False)

    return report


if __name__ == "__main__":
    pregunta_01()