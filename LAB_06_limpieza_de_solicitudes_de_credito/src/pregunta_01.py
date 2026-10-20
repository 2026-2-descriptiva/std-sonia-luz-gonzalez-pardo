def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    raise NotImplementedError

from pathlib import Path
import pandas as pd


def pregunta_01():
    """
    Limpia el archivo `data/solicitudes_de_credito.csv.gz` y guarda el resultado
    en `submission/solicitudes_de_credito.csv`.
    """
    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "solicitudes_de_credito.csv.gz"
    submission_dir = base_dir / "submission"
    submission_dir.mkdir(parents=True, exist_ok=True)

    # 1. Leer CSV omitiendo la columna de índice irrelevante (index_col=0 o sep=";")
    df = pd.read_csv(data_path, sep=";", index_col=0)

    # 2. Eliminar filas donde faltan datos (excepto en comuna_ciudadano)
    columnas_sin_comuna = [col for col in df.columns if col != "comuna_ciudadano"]
    df = df.dropna(subset=columnas_sin_comuna)

    # 3. Limpieza de campos de texto
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for col in columnas_texto:
        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.replace("-", " ")
            .str.replace("_", " ")
            .str.strip()
        )

    # 4. Limpieza de estrato (entero)
    df["estrato"] = df["estrato"].astype(int)

    # 5. Limpieza de monto_del_credito (eliminar $, comas, .00 y convertir a entero)
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .str.strip()
        .astype(int)
    )

    # 6. Normalización de fecha_de_beneficio a YYYY-MM-DD
    # Manejar formatos mixtos (DD/MM/YYYY y YYYY/MM/DD)
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    ).fillna(
        pd.to_datetime(df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce")
    ).dt.strftime("%Y-%m-%d")

    # 7. Eliminar registros duplicados
    df = df.drop_duplicates()

    # 8. Reordenar las columnas al orden estricto solicitado
    columnas_ordenadas = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]
    df = df[columnas_ordenadas]

    # 9. Guardar CSV final
    output_path = submission_dir / "solicitudes_de_credito.csv"
    df.to_csv(output_path, sep=";", index=False)


if __name__ == "__main__":
    pregunta_01()
