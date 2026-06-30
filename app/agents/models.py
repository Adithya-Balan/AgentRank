from sqlalchemy import Boolean, Column, DateTime, Float, Integer, JSON, String

from app.db.database import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    category = Column(String, index=True)
    framework = Column(String)
    endpoint = Column(String, nullable=False, unique=True, index=True)
    wallet_address = Column(String, index=True)
    pricing_model = Column(String, default="free")
    price_per_call = Column(Float, default=0.0)
    capabilities = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    health_status = Column(String, default="unknown")
    last_checked_at = Column(DateTime(timezone=True))
    last_response_time_ms = Column(Float)
    last_error = Column(String)
    consecutive_failures = Column(Integer, default=0)
    trust_score = Column(Float, default=0.0)
    staked_tokens = Column(Float, default=0.0)
