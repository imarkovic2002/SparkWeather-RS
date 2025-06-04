from pydantic import BaseModel
from typing import Dict

class TrendResponse(BaseModel):
    vrijednosti:Dict[str, float]