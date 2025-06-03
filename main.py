from fastapi import FastAPI
from analytics.routes import router as analytics_router
from filter.routes import router as filter_router

app = FastAPI(
    title="SparkWeather API",
    description="Distribuirani sustav za analizu vremenskih podataka korištenjem PySparka.",
)

# Uključivanje ruta iz različitih modula
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(filter_router, prefix="/filter", tags=["Filter"])