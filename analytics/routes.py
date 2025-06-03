from fastapi import APIRouter, HTTPException
from .spark_jobs import get_average_by_country, get_median_temperature_by_country
from .models import CountryMedian, CountryTemperature

router = APIRouter()

@router.get("/average_country", response_model=CountryTemperature)
def average_country(drzava: str):
    result = get_average_by_country(drzava)
    if result is None:
        raise HTTPException(status_code=404, detail='Nema podataka za tu državu.')
    return CountryTemperature(država=drzava, prosječna_temperatura=result)

@router.get("/median_country", response_model=CountryMedian)
def median_country(drzava: str):
    result = get_median_temperature_by_country(drzava)
    if result is None:
        raise HTTPException(status_code=404, detail="Nema podataka za tu državu.")
    return CountryMedian(država=drzava, medijan_temperatura=result)