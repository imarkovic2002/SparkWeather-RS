from pydantic import BaseModel
from typing import List

class WeatherEntry(BaseModel):
    datum: str
    grad: str
    drzava: str
    temperatura: float