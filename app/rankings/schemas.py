from pydantic import BaseModel

class RankedAgent(BaseModel):
    agent_id: int
    name: str
    category: str | None
    price_per_call: float
    overall_trust_score: float
    reliability_score: float | None
    latency_score: float | None
    health_status: str
    capabilities: list[str]

    model_config = {"from_attributes": True}


class RankingResponse(BaseModel):
    results: list[RankedAgent]
    total_found: int
