from fastapi import FastAPI, HTTPException
import polars as pl
from contextlib import asynccontextmanager

lazy_df = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global lazy_df
    print("Initializing Polars LazyFrame...")
    # scan_csv does not load the file into memory; it just reads metadata
    lazy_df = pl.scan_csv("/app/data/dataset.csv")
    yield
    lazy_df = None

app = FastAPI(lifespan=lifespan, title="Polars Lazy API")

@app.get("/aggregate/{category}")
async def aggregate_data(category: str):
    if category not in ["A", "B", "C", "D", "E"]:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    # Lazy execution: builds the query plan, multithreads execution on collect()
    query = (
        lazy_df
        .filter(pl.col("category") == category)
        .select((pl.col("value") * pl.col("multiplier")).mean().alias("mean_val"))
    )
    
    result = query.collect()
    
    return {"engine": "polars", "category": category, "aggregated_mean": result["mean_val"][0]}