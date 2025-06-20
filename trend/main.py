from fastapi import FastAPI
from routes import router as trend_router

app = FastAPI(
    title="Trend Microservice",
    description="Mikroservis za praćenja trenda vremenskih podataka.",
    root_path="/trend" 
)

app.include_router(trend_router, tags=["Trend"])