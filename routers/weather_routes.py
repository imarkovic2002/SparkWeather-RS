from fastapi import APIRouter, HTTPException
from .spark_jobs import (
    get_average_by_country,
    get_monthly_avg_by_city,
    get_invalid_temperature_records,
    get_warmest_days,
    get_variable_trend,
    filter_data_by_city_and_year,
    get_median_temperature_by_country,
)

router = APIRouter()

@router.get("/")
def main_root():
    return {'Message': 'SparkWeather API radi!!'}


@router.get("/average_country")
def average_country(drzava:str):
    result = get_average_by_country(drzava)
    if result is None:
        raise HTTPException(status_code=404, detail="Nema podataka za tu državu.")
    return {"država": drzava, 
            "prosječna temperatura": result}

@router.get("/monthly_average")
def monthly_average(grad:str):
    result = get_monthly_avg_by_city(grad)
    if result is None:
        raise HTTPException(status_code=404, detail="Nisu pronađeni podaci za taj grad.")
    return result

@router.get("/invalid_data")
def invalid_data():
    result = get_invalid_temperature_records()
    if not result:
        return {'message': 'Nema nelogičnih podataka.'}
    return result

@router.get("/trend")
def trend(varijabla: str, grad: str = None):
    result = get_variable_trend(varijabla, grad)
    if not result:
        raise HTTPException(status_code=404, detail="Nema podataka za zadani upit.")
    return result


@router.get("/warmest_days")
def warmest_days(grad: str, n: int = 5):
    result = get_warmest_days(grad, n)
    if not result:
        raise HTTPException(status_code=404, detail="Taj grad ne postoji.")
    return result

@router.get("/filter")
def filter_by_city_and_year(grad: str, godina: int):
    result = filter_data_by_city_and_year(grad, godina)
    if not result:
        raise HTTPException(status_code=404, detail="Nema podataka za taj grad i godinu.")
    return result

@router.get("/median_country")
def median_country(drzava: str):
    result = get_median_temperature_by_country(drzava)
    if result is None:
        raise HTTPException(status_code=404, detail="Nema podataka za tu državu.")
    return {
        "država": drzava,
        "medijan temperature": result
    }
