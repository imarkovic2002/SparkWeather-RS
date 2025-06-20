from fastapi import APIRouter, HTTPException
from spark_jobs import filter_by_city_and_year, get_extreme_temperatures, get_weather_extremes, remove_extreme_temperatures
from models import WeatherEntry, ExtremeTemperatureResponse, WeatherExtremesResponse
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

@router.get("/weather_extremes", response_model=WeatherExtremesResponse)
async def weather_extremes():
    return await get_weather_extremes()

@router.delete("/delete/extreme-temperatures")
async def delete_extreme_temperatures(threshold_high: float = 60.0, threshold_low: float = -50.0):
    broj_brisanih = await remove_extreme_temperatures(threshold_low, threshold_high)
    return {"poruka": f"Obrisano je {broj_brisanih} zapisa s ekstremnim temperaturama."}