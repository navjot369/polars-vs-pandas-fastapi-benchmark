from fastapi import FastAPI, HTTPException
import pandas as pd
from contextlib import asynccontextmanager

# Global variable to hold the DataFrame in memory
df = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global df
    print("Loading dataset into Pandas memory...")
    df = pd.read_csv("/app/data/dataset.csv")
    yield
    df = None

app = FastAPI(lifespan=lifespan, title="Pandas Eager API")

@app.get("/aggregate/{category}")
async def aggregate_data(category: str):
    if category not in ["A", "B", "C", "D", "E"]:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    # Eager execution: blocks the thread while calculating
    filtered_df = df[df["category"] == category]
    result = (filtered_df["value"] * filtered_df["multiplier"]).mean()
    
    return {"engine": "pandas", "category": category, "aggregated_mean": float(result)}