from fastapi import APIRouter, HTTPException, Query
from spark_jobs import get_variable_trend, get_multiple_variable_trends,get_weekly_trend
from models import TrendResponse, MultiTrendResponse
from typing import Optional, List, Dict

router = APIRouter()

@router.get("/", response_model=TrendResponse)
def trend_vrijednosti( 
    varijabla: str = Query(..., description="npr. temperatura, vlaga, tlak"),
    grad: str = Query(None)
):
    result = get_variable_trend(varijabla, grad)
    if result is None:
        raise HTTPException(status_code=400, detail="Nepostojeća varijabla ili grad.")
    return {"vrijednosti": result}

@router.get("/multi_trend", response_model=MultiTrendResponse)
def multi_trend(
    varijable: List[str] = Query(..., description="Lista varijabli npr. temperatura, vlaga, tlak"),
    grad: Optional[str] = Query(None, description="Naziv grada")
):
    result = get_multiple_variable_trends(varijable, grad)
    if result is None:
        raise HTTPException(status_code=400, detail="Neke varijable nisu pronađene.")
    if result == {}:
        raise HTTPException(status_code=404, detail="Nema podataka za zadani grad.")
    
    return {"grad": grad if grad else "Svi gradovi", "trendovi": result}

@router.get("/weekly", response_model = TrendResponse)
def tjedni_trend(varijabla: str = Query(..., description="temperatura, tlak, vlaga"), 
                 grad: Optional[str] = Query(None),
                 godina: Optional[int] = Query(None, description="npr. 2021")
                 ):
    result = get_weekly_trend(varijabla, grad, godina)
    if result is None:
        raise HTTPException(status_code=400, detail="Varijabla ili grad ne postoji. Ili ne postoje podaci za tu godinu")
    return {"vrijednosti": result} 