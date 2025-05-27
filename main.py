from fastapi import FastAPI, HTTPException
import pandas as pd

weather_df = pd.read_csv("weather_data.csv", parse_dates=["datum"])

app = FastAPI()

@app.get("/")
def main_root():
    return {'Message': 'Hello'}

@app.get("/proba")
def get_random_data():
    if weather_df.empty:
        raise HTTPException(status_code=404, detail="CSV podaci nisu dostupni")
    
    sample = weather_df.sort_values("datum").head(5)
    return sample.to_dict(orient="records")

@app.get("/average_country")
def average_per_country(drzava:str):
    df = weather_df[weather_df["država"] == drzava]
    if df.empty:
        raise HTTPException(status_code=404, detail="Nema podataka za tu državu.")
    return {
        "država":drzava,
        "prosječna temperatura": round(df["temperatura"].mean(), 2)
    }

@app.get("/filter")
def filter_data(grad: str, godina: int):
        df = weather_df [(weather_df["grad"].str.lower() == grad.lower()) & (weather_df["datum"].dt.year == godina) ]
    if df.empty:
        raise HTTPException(status_code=404, detail="Nema podataka za taj grad ili godinu.")
    return df.head(10).to_dict(orient="records")