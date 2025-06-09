from pydantic import BaseModel
from typing import Dict, List

class TrendResponse(BaseModel):
    vrijednosti:Dict[str, float]

class MultiTrendResponse(BaseModel):
    grad: str
    trendovi: Dict[str, Dict[str, float]]