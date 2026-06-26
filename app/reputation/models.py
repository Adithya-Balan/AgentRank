from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class AgentInteraction(Base):
    __tablename__ = "agent_interactions"

    id = Column(Integer, primary_key=True, index=True)
    source_agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    target_agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    
    interaction_type = Column(String, default="hire", index=True)
    success = Column(Boolean, default=True)
    task_description = Column(String)
    cost_incurred = Column(Float, default=0.0)
    latency_ms = Column(Float, default=0.0)
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    
    source_agent = relationship("Agent", foreign_keys=[source_agent_id])
    target_agent = relationship("Agent", foreign_keys=[target_agent_id])
