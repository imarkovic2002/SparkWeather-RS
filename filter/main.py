from fastapi import FastAPI
from routes import router as filter_router

app = FastAPI(
    title="Filter Microservice",
    description="Mikroservis za filtriranje vremenskih podataka."
)

app.include_router(filter_router, prefix="/filter", tags=["Filter"])
