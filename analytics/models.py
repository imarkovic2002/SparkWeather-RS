from pydantic import BaseModel
from typing import Dict

class CountryTemperature(BaseModel):
    drzava: str
    prosjecna_temperatura: float

class CountryMedian(BaseModel):
    drzava: str
    medijan_temperatura: float

class MonthlyAverageResponse(BaseModel):
    mjesecne_vrijednosti: Dict[int, float]