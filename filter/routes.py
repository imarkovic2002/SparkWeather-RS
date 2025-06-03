from fastapi import APIRouter, HTTPException
from filter.spark_jobs import filter_by_city_and_year
from filter.models import WeatherEntry 

router = APIRouter()

@router.get("/filter", response_model=list[WeatherEntry])
def filter_weather_data(grad: str, godina: int):
    result = filter_by_city_and_year(grad, godina)
    if not result:
        raise HTTPException(status_code=404, detail="Nema podataka za taj grad ili godinu.")
    return result