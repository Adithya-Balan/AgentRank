from datetime import datetime
from pydantic import BaseModel

class DomainTrustRead(BaseModel):
    domain: str
    mu: float
    sigma: float
    last_evaluated_at: datetime
    
    model_config = {"from_attributes": True}

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
    domain_trusts: list[DomainTrustRead] = []

    model_config = {"from_attributes": True}
