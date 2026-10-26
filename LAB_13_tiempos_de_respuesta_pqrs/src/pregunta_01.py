import pandas as pd
import os
import numpy as np

def _load_channel(path: str, channel: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Filas idénticas = misma solicitud repetida. Las filas sin record_id se conservan.
    df = df.drop_duplicates().copy()
    df["channel"] = channel
    return df
 
 
def _add_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df["in_date"] = pd.to_datetime(df["in_date"]).dt.normalize()
    df["out_date"] = pd.to_datetime(df["out_date"]).dt.normalize()
 
    df["answered"] = df["out_date"].notna()
 
    df["calendar_days"] = (df["out_date"] - df["in_date"]).dt.days
 
    # Días hábiles en el intervalo (in_date, out_date]: busday_count cuenta [a, b),
    # así que se desplazan ambos extremos un día.
    df["business_days"] = np.nan
    ans = df["answered"]
    start = (df.loc[ans, "in_date"] + pd.Timedelta(days=1)).values.astype("datetime64[D]")
    end = (df.loc[ans, "out_date"] + pd.Timedelta(days=1)).values.astype("datetime64[D]")
    df.loc[ans, "business_days"] = np.busday_count(start, end)
 
    # Pendientes no cumplen el plazo.
    df["on_time"] = ans & (df["business_days"] <= 15)
    df["year"] = df["in_date"].dt.year
    return df
 
 
def _summary(g):
    return pd.Series(
        {
            "requests": len(g),
            "answered": int(g["answered"].sum()),
            "pending": int((~g["answered"]).sum()),
            "median_calendar_days": g.loc[g["answered"], "calendar_days"].median(),
            "median_business_days": g.loc[g["answered"], "business_days"].median(),
            "on_time_rate": g["on_time"].mean(),
        }
    )
 
 
def _resolve_paths() -> tuple[str, list[str]]:
    """Ubica la carpeta data/ y las carpetas submission/ igual que en el lab de cohortes.
 
    Estructura esperada:  <repo>/data/...  y  <repo>/src/pregunta_01.py
    """
    file_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(file_dir)
 
    candidates = [
        (os.path.join(base_dir, "data"), os.path.join(base_dir, "src", "submission")),
        (os.path.join(file_dir, "data"), os.path.join(file_dir, "submission")),
        ("data", "submission"),
    ]
    for data_dir, submission_dir in candidates:
        if os.path.exists(os.path.join(data_dir, "historical_requests_web.csv.gz")):
            break
    else:
        data_dir, submission_dir = "data", "submission"
 
    # Se escribe en submission/ del directorio actual (lo que suele revisar el
    # autograder) y en la carpeta junto al código, sin repetir si coinciden.
    submission_dirs = []
    for d in ["submission", submission_dir]:
        if os.path.abspath(d) not in [os.path.abspath(x) for x in submission_dirs]:
            submission_dirs.append(d)
    return data_dir, submission_dirs
 
 
def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    
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
    
    data_dir, submission_dirs = _resolve_paths()
    web = _load_channel(os.path.join(data_dir, "historical_requests_web.csv.gz"), "web")
    letter = _load_channel(
        os.path.join(data_dir, "historical_requests_letter.csv.gz"), "letter"
    )
    df = _add_metrics(pd.concat([letter, web], ignore_index=True))
 
    # 1. Resumen por canal
    channel_summary = (
        df.groupby("channel").apply(_summary).reset_index().sort_values("channel")
    )
    channel_summary = channel_summary[
        ["channel", "requests", "answered", "pending", "median_business_days", "on_time_rate"]
    ]
 
    # 2. Resumen por año y canal
    yearly_summary = (
        df.groupby(["year", "channel"]).apply(_summary).reset_index()
        .sort_values(["year", "channel"])
    )
    yearly_summary = yearly_summary[["year", "channel", "requests", "pending", "on_time_rate"]]
 
    # 3. Resumen por día de entrada (ambos canales), de lunes a domingo
    entry_day_summary = df.groupby("day_name").apply(_summary).reset_index()
    weekday_order = df.groupby("day_name")["in_date"].agg(lambda s: s.dt.dayofweek.mode()[0])
    entry_day_summary["_order"] = entry_day_summary["day_name"].map(weekday_order)
    entry_day_summary = entry_day_summary.sort_values("_order")[
        ["day_name", "requests", "median_calendar_days", "median_business_days"]
    ]
 
    tables = [channel_summary, yearly_summary, entry_day_summary]
    for t in tables:
        t.reset_index(drop=True, inplace=True)
        for col in ["requests", "answered", "pending", "year"]:
            if col in t.columns:
                t[col] = t[col].astype(int)
 
    for out_dir in submission_dirs:
        os.makedirs(out_dir, exist_ok=True)
        channel_summary.to_csv(os.path.join(out_dir, "channel_summary.csv"), index=False)
        yearly_summary.to_csv(os.path.join(out_dir, "yearly_summary.csv"), index=False)
        entry_day_summary.to_csv(
            os.path.join(out_dir, "entry_day_summary.csv"), index=False
        )
 
    return channel_summary, yearly_summary, entry_day_summary
 
 
if __name__ == "__main__":
    for t in pregunta_01():
        print(t, "\n")