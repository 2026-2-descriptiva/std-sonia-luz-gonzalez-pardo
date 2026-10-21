import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    raise NotImplementedError
import os
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    # 1. Determinar rutas relativas de lectura y escritura
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "superstore_orders.csv.gz")
    submission_dir = os.path.join(base_dir, "src", "submission")

    if not os.path.exists(data_path):
        data_path = "data/superstore_orders.csv.gz"
        submission_dir = "submission"

    # También aseguramos la creación de 'submission' en la raíz por compatibilidad
    os.makedirs("submission", exist_ok=True)
    os.makedirs(submission_dir, exist_ok=True)

    # 2. Cargar datos especificando el separador ';' y decimal ','
    df = pd.read_csv(data_path, sep=";", decimal=",")

    # -------------------------------------------------------------------------
    # TABLA 1: profitability_summary.csv
    # -------------------------------------------------------------------------
    lines = len(df)
    orders = df["Order ID"].nunique()
    sales = df["Sales"].sum()
    profit = df["Profit"].sum()
    profit_margin = profit / sales if sales != 0 else 0.0

    loss_df = df[df["Profit"] < 0]
    loss_lines = len(loss_df)
    loss_line_rate = loss_lines / lines if lines != 0 else 0.0
    lost_profit = abs(loss_df["Profit"].sum())

    df_profitability = pd.DataFrame(
        [
            {
                "lines": lines,
                "orders": orders,
                "sales": sales,
                "profit": profit,
                "profit_margin": profit_margin,
                "loss_lines": loss_lines,
                "loss_line_rate": loss_line_rate,
                "lost_profit": lost_profit,
            }
        ]
    )

    cols_profitability = [
        "lines",
        "orders",
        "sales",
        "profit",
        "profit_margin",
        "loss_lines",
        "loss_line_rate",
        "lost_profit",
    ]
    df_profitability = df_profitability[cols_profitability]

    # Exportar a ambas rutas para evitar discrepancias en los tests
    df_profitability.to_csv("submission/profitability_summary.csv", index=False)
    df_profitability.to_csv(
        os.path.join(submission_dir, "profitability_summary.csv"), index=False
    )

    # -------------------------------------------------------------------------
    # TABLA 2: discount_summary.csv
    # -------------------------------------------------------------------------
    def assign_discount_band(discount):
        if discount == 0:
            return "0%"
        elif 0 < discount <= 0.05:
            return "1%-5%"
        elif 0.05 < discount <= 0.10:
            return "6%-10%"
        else:
            return "más de 10%"

    df["discount_band"] = df["Discount"].apply(assign_discount_band)
    bands_order = ["0%", "1%-5%", "6%-10%", "más de 10%"]

    discount_rows = []
    for band in bands_order:
        band_df = df[df["discount_band"] == band]
        b_lines = len(band_df)
        b_sales = band_df["Sales"].sum()
        b_profit = band_df["Profit"].sum()
        b_profit_margin = b_profit / b_sales if b_sales != 0 else 0.0

        b_loss_df = band_df[band_df["Profit"] < 0]
        b_loss_lines = len(b_loss_df)
        b_loss_line_rate = b_loss_lines / b_lines if b_lines != 0 else 0.0
        b_lost_profit = abs(b_loss_df["Profit"].sum())

        discount_rows.append(
            {
                "discount_band": band,
                "lines": b_lines,
                "sales": b_sales,
                "profit": b_profit,
                "profit_margin": b_profit_margin,
                "loss_line_rate": b_loss_line_rate,
                "lost_profit": b_lost_profit,
            }
        )

    df_discount = pd.DataFrame(discount_rows)
    cols_discount = [
        "discount_band",
        "lines",
        "sales",
        "profit",
        "profit_margin",
        "loss_line_rate",
        "lost_profit",
    ]
    df_discount = df_discount[cols_discount]

    df_discount.to_csv("submission/discount_summary.csv", index=False)
    df_discount.to_csv(
        os.path.join(submission_dir, "discount_summary.csv"), index=False
    )

    # -------------------------------------------------------------------------
    # TABLA 3: priority_segments.csv
    # -------------------------------------------------------------------------
    segment_rows = []
    grouped = df.groupby(["Customer Segment", "Product Category"])

    for (segment, category), group in grouped:
        g_lines = len(group)
        if g_lines >= 100:
            g_sales = group["Sales"].sum()
            g_profit = group["Profit"].sum()
            g_profit_margin = g_profit / g_sales if g_sales != 0 else 0.0

            g_loss_df = group[group["Profit"] < 0]
            g_lost_profit = abs(g_loss_df["Profit"].sum())

            segment_rows.append(
                {
                    "Customer Segment": segment,
                    "Product Category": category,
                    "lines": g_lines,
                    "sales": g_sales,
                    "profit": g_profit,
                    "profit_margin": g_profit_margin,
                    "lost_profit": g_lost_profit,
                }
            )

    df_priority = pd.DataFrame(segment_rows)
    df_priority = df_priority.sort_values(
        by="lost_profit", ascending=False
    ).head(5)

    cols_priority = [
        "Customer Segment",
        "Product Category",
        "lines",
        "sales",
        "profit",
        "profit_margin",
        "lost_profit",
    ]
    df_priority = df_priority[cols_priority]

    df_priority.to_csv("submission/priority_segments.csv", index=False)
    df_priority.to_csv(
        os.path.join(submission_dir, "priority_segments.csv"), index=False
    )

    return df_profitability, df_discount, df_priority


if __name__ == "__main__":
    pregunta_01()