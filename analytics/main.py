from fastapi import FastAPI
from routes import router as analytics_router

app = FastAPI(
    title="Analytics Microservice",
    description="Mikroservis za analizu vremenskih podataka."
)

app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])