from fastapi import APIRouter, HTTPException
from filter.spark_jobs import filter_by_city_and_year, get_extreme_temperatures
from filter.models import WeatherEntry, ExtremeTemperatureResponse
from typing import List

router = APIRouter()

@router.get("/filter", response_model=list[WeatherEntry])
def filter_weather_data(grad: str, godina: int):
    result = filter_by_city_and_year(grad, godina)
    if not result:
        raise HTTPException(status_code=404, detail="Nema podataka za taj grad ili godinu.")
    return result

@router.get("/extreme_temperatures", response_model=ExtremeTemperatureResponse)
async def extreme_temperatures(grad: str):
    result = await get_extreme_temperatures(grad)
    if result is None:
        raise HTTPException(status_code=404, detail="Grad nije pronađen.")
    return result