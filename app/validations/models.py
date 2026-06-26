from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base


class ValidationReport(Base):
    __tablename__ = "validation_reports"

    id = Column(Integer, primary_key=True, index=True)
    benchmark_id = Column(Integer, ForeignKey("benchmark_results.id"), nullable=False, index=True, unique=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    
    factual_accuracy_score = Column(Float, nullable=False, default=0.0)
    hallucination_rate = Column(Float, nullable=False, default=0.0)
    citation_reliability_score = Column(Float, nullable=False, default=0.0)
    prompt_adherence_score = Column(Float, nullable=False, default=0.0)
    consistency_score = Column(Float, nullable=False, default=0.0)
    reasoning_quality_score = Column(Float, nullable=False, default=0.0)
    economic_efficiency_score = Column(Float, nullable=False, default=0.0)
    
    overall_validation_score = Column(Float, nullable=False, default=0.0)
    
    details = Column(JSON, default=dict)
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    benchmark = relationship("BenchmarkResult")
    agent = relationship("Agent")
