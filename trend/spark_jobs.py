from pyspark.sql.functions import to_date, col, avg, weekofyear, year
from session.spark_session import get_spark_session
from typing import Optional, List, Dict

spark = get_spark_session()

df = spark.read.csv("weather_data.csv", header=True, inferSchema=True)
df = df.withColumn("datum", to_date(col("datum"), "yyyy-MM-dd"))

def get_variable_trend(varijabla:str, grad:Optional[str] = None):
    if varijabla not in df.columns:
        return None
    
    filtered = df 
    if grad: 
        filtered = filtered.filter(col("grad") == grad)
        if filtered.count() == 0:
            return None
        
    trend_df = filtered.groupBy("datum").agg(avg(varijabla).alias("vrijednost")).orderBy("datum")
    trend_data = trend_df.tail(30)

    result = {str(row["datum"]): round(row["vrijednost"], 2) for row in trend_data}
    return result

def get_multiple_variable_trends(varijable: List[str], grad: Optional[str] = None) -> Optional[Dict[str, Dict[str, float]]]:
    invalid_vars = [var for var in varijable if var not in df.columns]
    if invalid_vars:
        return None

    filtered = df
    if grad:
        filtered = filtered.filter(col("grad") == grad)
        if filtered.count() == 0:
            return {}

    trendovi = {}

    for varijabla in varijable:
        trend_df = filtered.groupBy("datum").agg(avg(varijabla).alias("vrijednost")).orderBy("datum")
        trend_data = trend_df.tail(30)
        trendovi[varijabla] = {str(row["datum"]): round(row["vrijednost"], 2) for row in trend_data}

    return trendovi

def get_weekly_trend(varijabla: str, grad: Optional[str] = None, godina: Optional[int] = None):
    if varijabla not in df.columns: 
        return None
    data = df
    if grad:
        data = data.filter(col("grad") == grad)

    if godina:
        data = data.withColumn("godina", year(col("datum")))
        data = data.filter(col("godina") == godina)

        if data.count() == 0:
            return None
        data = data.withColumn("tjedan", weekofyear("datum"))
        trend_df = data.groupBy("tjedan").agg(avg(varijabla).alias("vrijednost")).orderBy("tjedan")
        result = {str(row["tjedan"]):round(row["vrijednost"], 2) for row in trend_df.collect()}
        return result
        