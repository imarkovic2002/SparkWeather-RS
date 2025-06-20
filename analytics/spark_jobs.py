from pyspark.sql.functions import col, avg, to_date, month, min, max, count, percentile_approx,stddev, year
from session.spark_session import get_spark_session
from models import SummaryResponse, MonthlyAverage, TopCity


spark = get_spark_session()

# Učitavanje CSV datoteke
df = spark.read.csv("weather_data.csv", header=True, inferSchema=True)
df = df.withColumn("datum", to_date(col("datum"), "yyyy-MM-dd"))

# prosjek temperature po državi
def get_average_by_country(drzava: str):
    filtered = df.filter(col("država") == drzava)
    if filtered.count() == 0:
        return None
    prosjek = filtered.select(avg("temperatura")).first()[0]
    return round(prosjek, 2)

# medijan temperature po državi
def get_median_temperature_by_country(drzava: str):
    filtered = df.filter(col("država") == drzava)
    if filtered.count() == 0:
        return None
    medijan = filtered.select(percentile_approx("temperatura", 0.5)).first()[0]
    return round(medijan, 2)

# prosječna temperatura po mjesecima za grad
def get_monthly_avg_temperature(grad: str):
    filtered = df.filter(col("grad") == grad)
    if filtered.count() == 0:
        return None
    with_month = filtered.withColumn("mjesec", month(col("datum")))
    mjesecni_prosjek = with_month.groupBy("mjesec").agg(avg("temperatura").alias("avg_temp"))
    results = mjesecni_prosjek.orderBy("mjesec").collect()
    return {row["mjesec"]: round(row["avg_temp"], 2) for row in results}


def get_summary_statistics():
    if df.limit(1).count() == 0:
        return {"error": "Nema podataka."}

    stats = df.select(
        min("temperatura").alias("minimum"),
        max("temperatura").alias("maksimum"),
        avg("temperatura").alias("prosjek"),
        stddev("temperatura").alias("standardna_devijacija")
    ).collect()[0]

    return {
        "minimum": stats["minimum"],
        "maksimum": stats["maksimum"],
        "prosjek": round(stats["prosjek"], 2),
        "standardna_devijacija": round(stats["standardna_devijacija"], 2)
    }

async def get_monthly_averages(godina: int):
    df_filtered = df.filter(year("datum") == godina)
    if df_filtered.count() == 0:
        return []

    df_monthly = df_filtered.withColumn("mjesec", month("datum"))
    result_df = df_monthly.groupBy("mjesec").agg(
        avg("temperatura").alias("prosjek")
    ).orderBy("mjesec")

    result = result_df.collect()
    return [
        MonthlyAverage(mjesec=row["mjesec"], prosjek=round(row["prosjek"], 2))
        for row in result
    ]

async def get_top_cities(broj: int, godina: int, mjerenje: str):
    if mjerenje not in df.columns:
        return []

    filtered = df.filter(year("datum") == godina)
    if filtered.count() == 0:
        return []

    avg_df = filtered.groupBy("grad").agg(
        avg(mjerenje).alias("prosjek")
    ).orderBy(col("prosjek").desc()).limit(broj)

    result = avg_df.collect()
    return [TopCity(grad=row["grad"], prosjek=round(row["prosjek"], 2)) for row in result]

# Statistika UV indeksa po mjesecima
async def get_monthly_uv_index_stats(godina: int):
    df_with_date = df.withColumn("mjesec", month(col("datum"))).withColumn("godina", year(col("datum")))
    filtered_df = df_with_date.filter(col("godina") == godina)

    stats = filtered_df.groupBy("mjesec").agg(avg("uv_index").alias("prosjek_uv"))
    result = {str(row["mjesec"]): round(row["prosjek_uv"], 2) for row in stats.collect()}
    return result