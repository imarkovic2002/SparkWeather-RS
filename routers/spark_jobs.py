from pyspark.sql import SparkSession
from pyspark.sql.functions import col,avg,month, to_date, desc, percentile_approx
import os

spark = SparkSession.builder \
    .appName("SparkWeatherjobs") \
    .getOrCreate()

DATA_PATH = os.getenv("DATA_PATH", "weather_data.csv")
df = spark.read.csv(DATA_PATH, header=True, inferSchema=True)

df = df.withColumn("datum", to_date(col("datum"), "yyyy-MM-dd"))

def get_average_by_country(drzava:str):
    filtered = df.filter(col("država") == drzava)
    if filtered.count() == 0:
        return None
    prosjek = filtered.select(avg("temperatura")).first()[0]
    return round(prosjek,2)

def get_monthly_avg_by_city(grad: str):
    filtered = df.filter(col("grad").ilike(grad))
    if filtered.count() == 0:
        return None
    with_month = filtered.withColumn("mjesec", month(col("datum")))
    grouped = with_month.groupBy("mjesec").agg(avg("temperatura").alias("avg_temp"))
    return {row["mjesec"]: round(row["avg_temp"], 2) for row in grouped.collect()}

def get_invalid_temperature_records():
    invalids = df.filter(col("temperatura") > 60).limit(20)
    return [row.asDict() for row in invalids.collect()]

def get_warmest_days(grad: str, n: int = 5):
    filtered = df.filter(col("grad").ilike(grad))
    if filtered.count() == 0:
        return []
    top_days = filtered.orderBy(col("temperatura").desc()).limit(n)
    return [row.asDict() for row in top_days.collect()]

def get_variable_trend(varijabla: str, grad: str = None):
    if varijabla not in df.columns:
        return None
    temp_df = df
    if grad:
        temp_df = temp_df.filter(col("grad").ilike(grad))
    if temp_df.count() == 0:
        return None
    grouped = temp_df.groupBy("datum").agg(avg(varijabla).alias("srednje"))
    result = grouped.orderBy(col("datum").desc()).limit(30).collect()
    return {row["datum"].strftime("%Y-%m-%d"): round(row["srednje"], 2) for row in reversed(result)}

def filter_data_by_city_and_year(grad: str, godina: int):
    filtered = df.filter(
        (col("grad").ilike(grad)) &
        (df["datum"].isNotNull()) &
        (df["datum"].substr(1, 4) == str(godina))
    )
    if filtered.count() == 0:
        return []
    return [row.asDict() for row in filtered.limit(10).collect()]

def get_median_temperature_by_country(drzava: str):
    filtered = df.filter(col("država") == drzava)
    if filtered.count() == 0:
        return None
    # Approximate median (50th percentile)
    medijan = filtered.select(percentile_approx("temperatura", 0.5)).first()[0]
    return round(medijan, 2)