from pyspark.sql.functions import to_date, col, year, min, max
from session.spark_session import get_spark_session
from filter.models import WeatherEntry, ExtremeTemperatureResponse, WeatherExtremesResponse, ExtremeWeatherMetric
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
        if "država" in row_dict:
            row_dict["drzava"] = row_dict.pop("država")
        row_dict.setdefault("drzava", "")
        result.append(WeatherEntry(**row_dict))
    return result

async def get_extreme_temperatures(grad: str):
    filtered = df.filter(col("grad") == grad)
    if filtered.count() == 0:
        return None

    min_temp_row = filtered.orderBy(col("temperatura").asc()).select("datum", "temperatura").first()
    max_temp_row = filtered.orderBy(col("temperatura").desc()).select("datum", "temperatura").first()

    return ExtremeTemperatureResponse(
        grad=grad,
        najniza_temp=min_temp_row["temperatura"],
        najnizi_dan=min_temp_row["datum"].isoformat(),
        najvisa_temp=max_temp_row["temperatura"],
        najvisi_dan=max_temp_row["datum"].isoformat(),
    )

async def get_weather_extremes():
    # najniza vidljivost
    row_vidljivost = df.select("grad", "vidljivost") \
        .orderBy(col("vidljivost").asc()).filter(col("vidljivost").isNotNull()).first()

    # kada ima najvise oborina
    row_oborine = df.select("grad", "oborine") \
        .orderBy(col("oborine").desc()).filter(col("oborine").isNotNull()).first()

    # ovo je najveća oblacnost
    row_oblacnost = df.select("grad", "oblacnost") \
        .orderBy(col("oblacnost").desc()).filter(col("oblacnost").isNotNull()).first()

    return WeatherExtremesResponse(
        najniza_vidljivost=ExtremeWeatherMetric(grad=row_vidljivost["grad"], vrijednost=row_vidljivost["vidljivost"]),
        najvise_oborina=ExtremeWeatherMetric(grad=row_oborine["grad"], vrijednost=row_oborine["oborine"]),
        najveca_oblacnost=ExtremeWeatherMetric(grad=row_oblacnost["grad"], vrijednost=row_oblacnost["oblacnost"])
    )