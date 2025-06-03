from pydantic import BaseModel

class CountryTemperature(BaseModel):
    država: str
    prosječna_temperatura: float

class CountryMedian(BaseModel):
    država: str
    medijan_temperatura: float