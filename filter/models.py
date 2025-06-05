from pydantic import BaseModel

class WeatherEntry(BaseModel):
    datum: str
    grad: str
    drzava: str
    temperatura: float

class ExtremeTemperatureResponse(BaseModel):
    grad: str
    najniza_temp: float
    najnizi_dan: str
    najvisa_temp: float
    najvisi_dan: str