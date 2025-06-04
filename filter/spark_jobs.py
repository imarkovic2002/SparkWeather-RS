from pyspark.sql.functions import to_date, col, year
from session.spark_session import get_spark_session
from filter.models import WeatherEntry
import datetime

spark = get_spark_session()

df = spark.read.csv("weather_data.csv", header=True, inferSchema=True)
df = df.withColumn("datum", to_date(col("datum"), "yyyy-MM-dd"))

def filter_by_city_and_year(grad: str, godina: int):
    df_with_year = df.withColumn("godina", year(col("datum")))
    filtered = df_with_year.filter((col("grad") == grad) & (col("godina") == godina))
    if filtered.count() == 0:
        return []
    records = filtered.limit(10).collect()
    result = []
    for row in records:
        row_dict = row.asDict()
        if "datum" in row_dict and isinstance(row_dict["datum"], (datetime.date, datetime.datetime)):
            row_dict["datum"] = row_dict["datum"].isoformat()
        row_dict.setdefault("drzava", "")
        result.append(WeatherEntry(**row_dict))
    return result
