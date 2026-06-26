from datetime import datetime
from pydantic import BaseModel, Field


class AgentInteractionCreate(BaseModel):
    source_agent_id: int
    target_agent_id: int
    interaction_type: str = Field(default="hire", max_length=50)
    success: bool = True
    task_description: str | None = Field(default=None, max_length=500)
    cost_incurred: float | None = Field(default=0.0, ge=0.0)
    latency_ms: float | None = Field(default=0.0, ge=0.0)


class AgentInteractionRead(AgentInteractionCreate):
    id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}


class ReputationGraphEdge(BaseModel):
    target_agent_id: int
    target_agent_name: str
    interaction_count: int
    success_rate: float
    average_latency_ms: float


class ReputationGraph(BaseModel):
    agent_id: int
    agent_name: str
    outbound_dependencies: list[ReputationGraphEdge]
    inbound_dependents: list[ReputationGraphEdge]
    network_reliability_score: float
