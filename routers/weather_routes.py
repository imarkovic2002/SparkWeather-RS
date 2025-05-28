from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import pandas as pd

weather_df = pd.read_csv("weather_data.csv", parse_dates=["datum"])

# Izbacivanje nelogičnih podataka
# weather_df = weather_df[weather_df["temperatura"] <= 60]

router = APIRouter()

@router.get("/")
def main_root():
    return {'Message': 'Hello'}

@router.get("/proba")
def get_random_data():
    if weather_df.empty:
        raise HTTPException(status_code=404, detail="CSV podaci nisu dostupni")
    
    sample = weather_df.sort_values("datum").head(5)
    return sample.to_dict(orient="records")

@router.get("/average_country")
def average_per_country(drzava:str):
    df = weather_df[weather_df["država"] == drzava]
    if df.empty:
        raise HTTPException(status_code=404, detail="Nema podataka za tu državu.")
    return {
        "država":drzava,
        "prosječna temperatura": round(df["temperatura"].mean(), 2)
    }

@router.get("/filter")
def filter_data(grad: str, godina: int):
    df = weather_df [(weather_df["grad"].str.lower() == grad.lower()) & (weather_df["datum"].dt.year == godina) ]
    if df.empty:
        raise HTTPException(status_code=404, detail="Nema podataka za taj grad ili godinu.")
    return df.head(10).to_dict(orient="records")

@router.get("/monthly_average")
def monthly_average(grad:str):
    df = weather_df [((weather_df["grad"].str.lower() == grad.lower()))]
    if df.empty:
        raise HTTPException(status_code=404, detail="Nisu pronađeni podaci za taj grad.")
    
    df["mjesec"] = df["datum"].dt.month
    grupirano = df.groupby("mjesec")["temperatura"].mean().round(2)

    return grupirano.to_dict()

@router.get("/neispravni")
def nelogicni_podaci():
    df = weather_df[weather_df["temperatura"] > 60]
    if df.empty:
        return {'message': 'Nema nelogičnih podataka.'}
    return df.head(20).to_dict(orient="records")

@router.get("/trend")
def trend_vrijednosti(
    varijabla: str = Query(..., description="npr. temperatura, vlaga, tlak"),
    grad: Optional[str] = None
):
    if varijabla not in weather_df.columns:
        raise HTTPException(status_code=400, detail=f"Nepostojeća varijabla: {varijabla}")

    df = weather_df.copy()
    if grad:
        df = df[df["grad"].str.lower() == grad.lower()]
        if df.empty:
            raise HTTPException(status_code=404, detail="Nema podataka za taj grad.")

    df["datum"] = pd.to_datetime(df["datum"])
    trend = df.groupby("datum")[varijabla].mean().round(2)
    return trend.tail(30).to_dict()  # ovo je da da zadnjih 30 dana, to mogu i promjeniti

@router.get("/warmest_days")
def the_warmest_days(grad: str, n: int = 5):
    df = weather_df[weather_df["grad"].str.lower() == grad.lower()]
    if df.empty:
        raise HTTPException(status_code=404, detail="Taj grad ne postoji.")
    top = df.sort_values("temperatura", ascending=False).head(n)
    return top.to_dict(orient="records")