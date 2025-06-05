from fastapi import APIRouter, HTTPException, Query
from .spark_jobs import (
    get_average_by_country,
    get_median_temperature_by_country,
    get_monthly_avg_temperature,
    get_summary_statistics,
    get_monthly_averages,
    get_top_cities,
)
from .models import (
    CountryTemperature,
    CountryMedian,
    MonthlyAverageResponse,
    SummaryResponse,
    MonthlyAverage,
    TopCity
)
from typing import List

router = APIRouter()

@router.get("/average_country", response_model=CountryTemperature)
def average_country(drzava: str):
    result = get_average_by_country(drzava)
    if result is None:
        raise HTTPException(status_code=404, detail="Nema podataka za tu državu.")
    return {"drzava": drzava, "prosjecna_temperatura": result}

@router.get("/median_country", response_model=CountryMedian)
def median_country(drzava: str):
    result = get_median_temperature_by_country(drzava)
    if result is None:
        raise HTTPException(status_code=404, detail="Nema podataka za tu državu.")
    return {"drzava": drzava, "medijan_temperatura": result}

@router.get("/monthly_average", response_model=MonthlyAverageResponse)
def monthly_average(grad: str):
    result = get_monthly_avg_temperature(grad)
    if result is None:
        raise HTTPException(status_code=404, detail="Nema podataka za taj grad.")
    return {"mjesecne_vrijednosti": result}

@router.get("/summary", response_model=SummaryResponse)
async def summary_analytics():
    result = get_summary_statistics()
    if not result:
        raise HTTPException(status_code=404, detail='Nema dostupnih podataka za ovu analizu.')
    return result

@router.get("/monthly-averages", response_model=List[MonthlyAverage])
async def monthly_averages(godina: int = Query(..., ge=2019, le=2024)):
    result = await get_monthly_averages(godina)
    if not result:
        raise HTTPException(status_code=404, detail=f"Nema podataka za godinu {godina}.")
    return result

@router.get("/top_cities", response_model=List[TopCity])
async def top_cities(
    broj: int = Query(5, ge=1, le=50),
    godina: int = Query(..., ge=2019, le=2024),
    mjerenje: str = Query("temperatura", regex="^(temperatura|vlaga|tlak|oborine)$")
):
    result = await get_top_cities(broj, godina, mjerenje)
    if not result:
        raise HTTPException(status_code=404, detail="Nema dostupnih podataka.")
    return result