from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, to_date, month, desc, percentile_approx

spark = SparkSession.builder \
    .appName("SparkWeather") \
    .getOrCreate()

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

# najtopliji dani u gradu
def get_top_warmest_days(grad: str, n: int = 5):
    filtered = df.filter(col("grad") == grad)
    if filtered.count() == 0:
        return []
    top_days = filtered.orderBy(desc("temperatura")).limit(n)
    return top_days.toPandas().to_dict(orient="records")

# trend varijable kroz vrijeme
def get_variable_trend(varijabla: str, grad: str = None):
    if varijabla not in df.columns:
        return None

    data = df
    if grad:
        data = data.filter(col("grad") == grad)
        if data.count() == 0:
            return None

    grouped = data.groupBy("datum").agg(avg(varijabla).alias("vrijednost"))
    results = grouped.orderBy("datum").collect()
    return {str(row["datum"]): round(row["vrijednost"], 2) for row in results[-30:]}  # zadnjih 30 dana
