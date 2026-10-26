import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Una tienda quiere saber si sus clientes vuelven a comprar después de su
    primera compra. Para responder, agrupe a los clientes en cohortes según
    el mes de su primera compra y mida, mes a mes, qué proporción de cada
    cohorte vuelve a comprar. Use `data/sales.csv.gz`, que tiene una fila por
    orden con su cliente (`CustomerID`) y su fecha (`OrderDate`).

    Use estas definiciones:

    - `cohort_month`: el mes de la primera compra del cliente, escrito como
      `AAAA-MM`.
    - `period_index`: los meses transcurridos desde `cohort_month`; es 0 en el
      mes de la primera compra, 1 en el mes siguiente, y así sucesivamente.
    - `active_customers`: la cantidad de clientes distintos de la cohorte que
      compraron en ese período.
    - `cohort_size`: la cantidad de clientes de la cohorte, es decir, sus
      clientes activos en el período 0.
    - `retention_rate`: `active_customers` sobre `cohort_size`.

    Genere dos archivos en `submission/`:

    1. `cohort_retention.csv`, sin el índice de Pandas, con las columnas
       `cohort_month`, `period_index`, `active_customers`, `cohort_size` y
       `retention_rate`, y una fila por cada combinación cohorte–período
       observada, ordenadas por cohorte y período.

    2. `cohort_retention_heatmap.png`, un mapa de calor de `retention_rate`
       con una fila por cohorte (eje vertical) y una columna por período
       (eje horizontal). Muestre los valores como porcentajes. Los períodos
       que todavía no se pueden observar para una cohorte no significan
       retención cero: déjelos vacíos en el mapa.

    La función también debe retornar la tabla de retención.

    Ejemplo del formato de `cohort_retention.csv`:

        cohort_month,period_index,active_customers,cohort_size,retention_rate
        2022-01,0,100,100,1.0
        2022-01,1,26,100,0.26
        ...
    """

    raise NotImplementedError

import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def build_cohort_analysis() -> pd.DataFrame:

    # 1. Determinar rutas relativas de lectura y entrega
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "sales.csv.gz")
    submission_dir = os.path.join(base_dir, "src", "submission")

    if not os.path.exists(data_path):
        data_path = "data/sales.csv.gz"
        submission_dir = "submission"

    os.makedirs("submission", exist_ok=True)
    os.makedirs(submission_dir, exist_ok=True)

    # 2. Cargar datos
    df = pd.read_csv(data_path)

    # Convertir a datetime
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])

    # Extraer el mes de la orden como Period de Pandas
    df["order_month"] = df["OrderDate"].dt.to_period("M")

    # Identificar el mes de la primera compra de cada cliente (cohort_month)
    df["cohort_month_period"] = df.groupby("CustomerID")["order_month"].transform(
        "min"
    )

    # Calcular period_index en cantidad de meses
    df["period_index"] = (
        (df["order_month"].dt.year - df["cohort_month_period"].dt.year) * 12
        + (df["order_month"].dt.month - df["cohort_month_period"].dt.month)
    )

    # Convertir el periodo a string con formato AAAA-MM
    df["cohort_month"] = df["cohort_month_period"].astype(str)

    # 3. Calcular clientes activos por cohorte y período
    cohort_data = (
        df.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index()
    )
    cohort_data.rename(columns={"CustomerID": "active_customers"}, inplace=True)

    # Obtener el tamaño de cada cohorte (clientes en period_index = 0)
    cohort_sizes = cohort_data[cohort_data["period_index"] == 0][
        ["cohort_month", "active_customers"]
    ].rename(columns={"active_customers": "cohort_size"})

    # Unir el tamaño de la cohorte al DataFrame
    df_retention = cohort_data.merge(cohort_sizes, on="cohort_month")

    # Calcular la tasa de retención
    df_retention["retention_rate"] = (
        df_retention["active_customers"] / df_retention["cohort_size"]
    )

    # Ordenar adecuadamente
    cols = [
        "cohort_month",
        "period_index",
        "active_customers",
        "cohort_size",
        "retention_rate",
    ]
    df_retention = df_retention[cols].sort_values(
        by=["cohort_month", "period_index"]
    )

    # Exportar CSV entregable
    df_retention.to_csv("submission/cohort_retention.csv", index=False)
    df_retention.to_csv(
        os.path.join(submission_dir, "cohort_retention.csv"), index=False
    )

    # -------------------------------------------------------------------------
    # Generar Mapa de Calor (Heatmap)
    # -------------------------------------------------------------------------
    heatmap_data = df_retention.pivot(
        index="cohort_month", columns="period_index", values="retention_rate"
    )

    plt.figure(figsize=(12, 8))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".1%",
        cmap="YlGnBu",
        cbar_kws={"label": "Retention Rate"},
    )
    plt.title("Cohort Retention Rate")
    plt.xlabel("Period Index")
    plt.ylabel("Cohort Month")
    plt.tight_layout()

    # Guardar gráfico entregable
    plt.savefig("submission/cohort_retention_heatmap.png", dpi=300)
    plt.savefig(
        os.path.join(submission_dir, "cohort_retention_heatmap.png"), dpi=300
    )
    plt.close()

    return df_retention


if __name__ == "__main__":
    build_cohort_analysis()