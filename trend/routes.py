from fastapi import APIRouter, HTTPException, Query
from trend.spark_jobs import get_variable_trend
from trend.models import TrendResponse

router = APIRouter()

@router.get("/trend", response_model=TrendResponse)
def trend_vrijednosti( 
    varijabla: str = Query(..., description="npr. temperatura, vlaga, tlak"),
    grad: str = Query(None)
):
    result = get_variable_trend(varijabla, grad)
    if result is None:
        raise HTTPException(status_code=400, detail="Nepostojeća varijabla ili grad.")
    return {"vrijednosti": result}