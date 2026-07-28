from pathlib import Path
import sqlite3
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import health
from src.api.routers import companies
from src.api.routers import sectors
from src.api.routers import peers
from src.api.routers import valuation
from src.api.routers import screener
from src.api.routers import market_cap
from src.api.routers import portfolio
from src.api.routers import documents

# ----------------------------------------------------
# APP
# ----------------------------------------------------

app = FastAPI(
    title="Nifty100 Analytics API",
    version="1.0",
    description="REST API for Nifty100 Analytics Dashboard",
)

# ----------------------------------------------------
# CORS
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# DATABASE
# ----------------------------------------------------

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(db_path)


# ----------------------------------------------------
# LOGGING MIDDLEWARE
# ----------------------------------------------------


@app.middleware("http")
async def log_requests(request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    print("=" * 60)
    print(request.method, request.url.path)
    print(f"Execution Time : {duration:.4f} sec")
    print("=" * 60)

    return response


# ----------------------------------------------------
# ROOT
# ----------------------------------------------------


@app.get("/")
def home():

    return {"project": "Nifty100 Analytics", "status": "Running"}


# ----------------------------------------------------
# ROUTERS
# ----------------------------------------------------

app.include_router(health.router, prefix="/api/v1", tags=["Health"])

app.include_router(companies.router, prefix="/api/v1", tags=["Companies"])


app.include_router(sectors.router, prefix="/api/v1", tags=["Sectors"])

app.include_router(peers.router, prefix="/api/v1", tags=["Peers"])

app.include_router(valuation.router, prefix="/api/v1", tags=["Valuation"])
app.include_router(screener.router, prefix="/api/v1", tags=["Screener"])

app.include_router(market_cap.router, prefix="/api/v1", tags=["Market Cap"])

app.include_router(portfolio.router, prefix="/api/v1", tags=["Portfolio"])

app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])
