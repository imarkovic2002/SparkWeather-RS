from fastapi import FastAPI
from routers.weather_routes import router as weather_router

app = FastAPI()
app.include_router(weather_router)