from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class TrustProfile(Base):
    __tablename__ = "trust_profiles"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), unique=True, nullable=False, index=True)
    
    accuracy_score = Column(Float, nullable=False, default=0.0)
    citation_quality_score = Column(Float, nullable=False, default=0.0)
    reliability_score = Column(Float, nullable=False, default=0.0)
    consistency_score = Column(Float, nullable=False, default=0.0)
    cost_efficiency_score = Column(Float, nullable=False, default=0.0)
    latency_score = Column(Float, nullable=False, default=0.0)
    consensus_alignment_score = Column(Float, nullable=False, default=0.0)
    
    overall_trust_score = Column(Float, nullable=False, default=0.0)
    
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    agent = relationship("Agent")
