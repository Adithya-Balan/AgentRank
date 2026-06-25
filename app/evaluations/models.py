from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class BenchmarkResult(Base):
    __tablename__ = "benchmark_results"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    benchmark_name = Column(String, nullable=False, index=True)
    task_type = Column(String, nullable=False, index=True)
    score = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)
    latency_ms = Column(Float)
    cost_usd = Column(Float)
    evaluator = Column(String, default="manual")
    prompt = Column(String)
    expected_output = Column(String)
    actual_output = Column(String)
    evidence = Column(JSON, default=dict)
    notes = Column(String)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    agent = relationship("Agent")
