from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

@dataclass
class AutopsyReport:
    id: str
    forecast_id: str
    predicted_value: float
    actual_value: float
    error_absolute: float
    error_percent: float
    causes: List[str]  # e.g., ["DATA", "MODEL", "EXTERNAL_EVENT"]
    details: Dict[str, Any]
    created_at: datetime


def create_autopsy(forecast_id: str, predicted: float, actual: float, causes: Optional[List[str]] = None, details: Optional[Dict[str, Any]] = None) -> AutopsyReport:
    causes = causes or []
    details = details or {}
    error_abs = actual - predicted
    error_pct = ((actual - predicted) / predicted) * 100 if predicted != 0 else float('inf')
    return AutopsyReport(
        id=str(uuid.uuid4()),
        forecast_id=forecast_id,
        predicted_value=predicted,
        actual_value=actual,
        error_absolute=error_abs,
        error_percent=error_pct,
        causes=causes,
        details=details,
        created_at=datetime.utcnow()
    )
