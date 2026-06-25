from datetime import datetime

from pydantic import BaseModel, Field


class BenchmarkResultCreate(BaseModel):
    benchmark_name: str = Field(..., min_length=1, max_length=160)
    task_type: str = Field(..., min_length=1, max_length=80)
    score: float = Field(..., ge=0, le=100)
    passed: bool
    latency_ms: float | None = Field(default=None, ge=0)
    cost_usd: float | None = Field(default=None, ge=0)
    evaluator: str | None = Field(default="manual", max_length=120)
    prompt: str | None = Field(default=None, max_length=4000)
    expected_output: str | None = Field(default=None, max_length=4000)
    actual_output: str | None = Field(default=None, max_length=4000)
    evidence: dict = Field(default_factory=dict)
    notes: str | None = Field(default=None, max_length=2000)


class BenchmarkResultRead(BenchmarkResultCreate):
    id: int
    agent_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TrustScoreExplanation(BaseModel):
    agent_id: int
    trust_score: float
    benchmark_count: int
    average_benchmark_score: float | None
    health_status: str
    health_score: float
    formula: str

