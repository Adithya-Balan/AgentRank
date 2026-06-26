from datetime import datetime
from pydantic import BaseModel

class TrustProfileRead(BaseModel):
    id: int
    agent_id: int
    accuracy_score: float
    citation_quality_score: float
    reliability_score: float
    consistency_score: float
    cost_efficiency_score: float
    latency_score: float
    consensus_alignment_score: float
    overall_trust_score: float
    updated_at: datetime

    model_config = {"from_attributes": True}
