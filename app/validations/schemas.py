from datetime import datetime
from pydantic import BaseModel, Field


class ValidationReportCreate(BaseModel):
    factual_accuracy_score: float = Field(..., ge=0.0, le=100.0)
    hallucination_rate: float = Field(..., ge=0.0, le=100.0)
    citation_reliability_score: float = Field(..., ge=0.0, le=100.0)
    prompt_adherence_score: float = Field(..., ge=0.0, le=100.0)
    consistency_score: float = Field(..., ge=0.0, le=100.0)
    reasoning_quality_score: float = Field(..., ge=0.0, le=100.0)
    economic_efficiency_score: float = Field(..., ge=0.0, le=100.0)
    details: dict = Field(default_factory=dict)


class ValidationReportRead(ValidationReportCreate):
    id: int
    benchmark_id: int
    agent_id: int
    overall_validation_score: float
    created_at: datetime

    model_config = {"from_attributes": True}
