"""
app.py — wires all 4 route files into one FastAPI application.
This is the file Uvicorn actually runs.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import latest, critical, history, grid

app = FastAPI(
    title="Energy Consumption Analytics & Grid Overload Detection API",
    description="Serves live grid load data, critical zone alerts, and historical trends.",
    version="1.0.0",
)

# CORS open for local dev (Power BI / any frontend can hit this).
# In a real prod deployment you'd lock allow_origins down to specific domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(latest.router, tags=["Latest"])
app.include_router(critical.router, tags=["Critical"])
app.include_router(history.router, tags=["History"])
app.include_router(grid.router, tags=["Grid Detail"])


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "GreenGrid API is running"}