import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Una autoridad aeronáutica publica cada año un ranking de aerolíneas según
    su tasa de demora, y algunas aerolíneas se quejan de que es injusto: las
    demoras se acumulan a lo largo del día, de modo que una aerolínea con
    muchos vuelos en la tarde y la noche parece peor aunque opere igual de
    bien que las demás. Su tarea es construir un ranking que tenga en cuenta
    la mezcla de horarios de cada aerolínea.

    El archivo `data/flights_by_carrier_day_hour.csv.gz` tiene los vuelos
    nacionales entre 2006 y 2008, agregados por año, mes, día de la semana,
    hora programada de salida (`scheduled_departure_hour`) y aerolínea
    (`reporting_airline`). Use las columnas `operated_flights` (vuelos
    operados) y `delayed_departure_15_flights` (vuelos que salieron con 15
    minutos o más de demora).

    Siga estos pasos:

    1. Calcule la tasa nacional de demora de cada hora programada de salida:
       vuelos demorados sobre vuelos operados, con todas las aerolíneas
       juntas.
    2. Para cada aerolínea, calcule las demoras esperadas: en cada hora,
       multiplique sus vuelos operados por la tasa nacional de esa hora, y
       sume sobre todas las horas. Son las demoras que tendría si en cada hora
       se comportara como el promedio nacional.
    3. Divida las demoras observadas entre las esperadas. Un valor mayor que 1
       significa que la aerolínea se demora más de lo que explican sus
       horarios.

    Genere dos archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `hourly_delay_rates.csv`, con una fila por hora, de 0 a 23:
       `scheduled_departure_hour`, `operated_flights`,
       `delayed_departure_15_flights` y `delay_rate`.

    2. `carrier_adjusted_delays.csv`, con una fila por aerolínea:
       `reporting_airline`, `operated_flights`,
       `delayed_departure_15_flights`, `delay_rate` (la tasa sin ajustar),
       `expected_delayed_flights`, `observed_to_expected_ratio`, `crude_rank`
       y `adjusted_rank`. Incluya solamente aerolíneas con al menos 100 000
       vuelos operados. `crude_rank` es la posición según `delay_rate` y
       `adjusted_rank` la posición según `observed_to_expected_ratio`; en
       ambos, 1 es la peor aerolínea. Ordene la tabla por `adjusted_rank`.

    Compare los dos rankings: las aerolíneas que cambian de posición son las
    que el ranking sin ajustar juzga mal por sus horarios.

    La función también debe retornar las dos tablas, en el mismo orden.

    Ejemplo del formato de `carrier_adjusted_delays.csv`:

        reporting_airline,operated_flights,...,crude_rank,adjusted_rank
        EV,819223,...,1,1
        ...
    """

    raise NotImplementedError

import os
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame]:

    # 1. Determinar rutas de lectura y entrega
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "flights_by_carrier_day_hour.csv.gz")
    submission_dir = os.path.join(base_dir, "src", "submission")

    if not os.path.exists(data_path):
        data_path = "data/flights_by_carrier_day_hour.csv.gz"
        submission_dir = "submission"

    os.makedirs("submission", exist_ok=True)
    os.makedirs(submission_dir, exist_ok=True)

    # 2. Cargar datos
    df = pd.read_csv(data_path)

    # -------------------------------------------------------------------------
    # TABLA 1: hourly_delay_rates.csv
    # -------------------------------------------------------------------------
    hourly = (
        df.groupby("scheduled_departure_hour", as_index=False)[
            ["operated_flights", "delayed_departure_15_flights"]
        ]
        .sum()
        .sort_values(by="scheduled_departure_hour")
    )

    hourly["delay_rate"] = (
        hourly["delayed_departure_15_flights"] / hourly["operated_flights"]
    )

    cols_hourly = [
        "scheduled_departure_hour",
        "operated_flights",
        "delayed_departure_15_flights",
        "delay_rate",
    ]
    hourly = hourly[cols_hourly]

    # Guardar entregable 1
    hourly.to_csv("submission/hourly_delay_rates.csv", index=False)
    hourly.to_csv(
        os.path.join(submission_dir, "hourly_delay_rates.csv"), index=False
    )

    # -------------------------------------------------------------------------
    # TABLA 2: carrier_adjusted_delays.csv
    # -------------------------------------------------------------------------
    # Mapear la tasa nacional horaria al dataframe general
    df_merged = df.merge(
        hourly[["scheduled_departure_hour", "delay_rate"]],
        on="scheduled_departure_hour",
        how="left",
    )

    # Demoras esperadas para cada registro
    df_merged["expected_delays"] = (
        df_merged["operated_flights"] * df_merged["delay_rate"]
    )

    # Agrupar por aerolínea
    carrier = (
        df_merged.groupby("reporting_airline", as_index=False)
        .agg(
            operated_flights=("operated_flights", "sum"),
            delayed_departure_15_flights=("delayed_departure_15_flights", "sum"),
            expected_delayed_flights=("expected_delays", "sum"),
        )
    )

    # Filtrar aerolíneas con al menos 100,000 vuelos operados
    carrier = carrier[carrier["operated_flights"] >= 100000].copy()

    # Tasas y ratios
    carrier["delay_rate"] = (
        carrier["delayed_departure_15_flights"] / carrier["operated_flights"]
    )
    carrier["observed_to_expected_ratio"] = (
        carrier["delayed_departure_15_flights"] / carrier["expected_delayed_flights"]
    )

    # Rankings (1 es la peor aerolínea -> mayor tasa/ratio)
    carrier["crude_rank"] = (
        carrier["delay_rate"].rank(ascending=False, method="min").astype(int)
    )
    carrier["adjusted_rank"] = (
        carrier["observed_to_expected_ratio"]
        .rank(ascending=False, method="min")
        .astype(int)
    )

    # Ordenar por adjusted_rank
    carrier = carrier.sort_values(by="adjusted_rank", ascending=True)

    cols_carrier = [
        "reporting_airline",
        "operated_flights",
        "delayed_departure_15_flights",
        "delay_rate",
        "expected_delayed_flights",
        "observed_to_expected_ratio",
        "crude_rank",
        "adjusted_rank",
    ]
    carrier = carrier[cols_carrier]

    # Guardar entregable 2
    carrier.to_csv("submission/carrier_adjusted_delays.csv", index=False)
    carrier.to_csv(
        os.path.join(submission_dir, "carrier_adjusted_delays.csv"), index=False
    )

    return hourly, carrier


if __name__ == "__main__":
    pregunta_01()
