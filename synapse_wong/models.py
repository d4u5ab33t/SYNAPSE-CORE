from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any
import uuid

Id = str

def new_id() -> Id:
    return str(uuid.uuid4())

@dataclass
class Source:
    id: Id = field(default_factory=new_id)
    name: str = ""
    type: str = ""  # e.g., "platform", "onchain", "creator"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Artifact:
    id: Id = field(default_factory=new_id)
    artifact_type: str = ""  # e.g., "audio_clip", "post", "tx"
    payload: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Evidence:
    id: Id = field(default_factory=new_id)
    artifact: Artifact = None
    source: Source = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metric: Dict[str, Any] = field(default_factory=dict)  # e.g., {"streams": 12000, "growth_pct": 340}
    community: Optional[str] = None
    related_event: Optional[str] = None
    transformation: Optional[str] = None  # e.g., "normalized_by_country"
    flagged: bool = False  # set by autopsy if evidence is unreliable

@dataclass
class Claim:
    id: Id = field(default_factory=new_id)
    text: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    evidences: List[Evidence] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)  # alt explanations
    confidence: Optional[float] = None  # posterior from Hypothesis Competition

@dataclass
class HypothesisScore:
    name: str
    prior: float
    likelihood: float
    posterior: float

@dataclass
class Forecast:
    id: Id = field(default_factory=new_id)
    target: str = ""
    horizon_days: int = 30
    probability: float = 0.0
    expected_growth: float = 0.0
    confidence: float = 0.0
    risks: List[str] = field(default_factory=list)
    falsification_test: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    origin_claim_id: Optional[Id] = None
    evidence_ids: List[Id] = field(default_factory=list)
