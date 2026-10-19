from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
import json
from pathlib import Path

app = FastAPI(title="WONG Forensic Core (minimal)")

# Load JSON schema for forecast validation
SCHEMA_PATH = Path(__file__).parent.parent / 'forecast_schema.json'
try:
    with open(SCHEMA_PATH, 'r') as f:
        FORECAST_SCHEMA = json.load(f)
except Exception:
    FORECAST_SCHEMA = None

class ForecastIn(BaseModel):
    target: str
    horizon_days: int = Field(..., gt=0)
    probability: float = Field(..., ge=0.0, le=1.0)
    expected_growth: float
    confidence: float = Field(..., ge=0.0, le=1.0)
    risks: Optional[List[str]] = []
    falsification_test: str

@app.get('/health')
async def health():
    return {"status": "ok"}

@app.post('/forecast')
async def create_forecast(f: ForecastIn):
    # minimal validation by pydantic; schema validation could be added
    return {"accepted": True, "forecast": f.dict()}

@app.post('/validate-forecast-schema')
async def validate_forecast_schema(payload: dict):
    if FORECAST_SCHEMA is None:
        raise HTTPException(status_code=500, detail="Forecast schema not found")
    # naive check: ensure required fields exist
    missing = [k for k in FORECAST_SCHEMA.get('required', []) if k not in payload]
    if missing:
        raise HTTPException(status_code=400, detail={"missing": missing})
    return {"valid": True}
