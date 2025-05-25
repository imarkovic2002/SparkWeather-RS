from fastapi import FastAPI
import pandas as pd

weather_df = pd.read_csv("weather_data.csv", parse_dates=["datum"])

app = FastAPI()

@app.get("/")
def main_root():
    return {'Message': 'Hello'}

@app.get("/proba")
def get_random_data():
    sample = weather_df.sort_values("datum").head(5)
    return sample.to_dict(orient="records")

