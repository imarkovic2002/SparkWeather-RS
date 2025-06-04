from pyspark.sql.functions import to_date, col, avg
from session.spark_session import get_spark_session
from typing import Optional

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