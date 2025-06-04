from fastapi import FastAPI
from analytics.routes import router as analytics_router
from filter.routes import router as filter_router
from trend.routes import router as trend_router
app = FastAPI(
    title="SparkWeather API",
    description="Distribuirani sustav za analizu vremenskih podataka korištenjem PySparka.",
)

# Uključivanje ruta iz različitih modula
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(filter_router, prefix="/filter", tags=["Filter"])
app.include_router(trend_router, prefix="/trend", tags=["Trend"])