from fastapi import APIRouter, HTTPException
from .spark_jobs import (
    get_average_by_country,
    get_median_temperature_by_country,
    get_monthly_avg_temperature,
)
from .models import (
    CountryTemperature,
    CountryMedian,
    MonthlyAverageResponse,
)

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