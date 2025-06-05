from pydantic import BaseModel
from typing import Dict, List

class CountryTemperature(BaseModel):
    drzava: str
    prosjecna_temperatura: float

class CountryMedian(BaseModel):
    drzava: str
    medijan_temperatura: float

class MonthlyAverageResponse(BaseModel):
    mjesecne_vrijednosti: Dict[int, float]

class SummaryResponse(BaseModel):
    prosjek: float
    standardna_devijacija: float
    minimum: float
    maksimum: float

class MonthlyAverage(BaseModel):
    mjesec:int
    prosjek:float

class TopCity(BaseModel):
    grad: str
    prosjek: float