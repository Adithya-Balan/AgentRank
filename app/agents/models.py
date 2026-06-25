from sqlalchemy import Boolean, Column, Float, Integer, JSON, String

from app.db.database import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    category = Column(String, index=True)
    framework = Column(String)
    endpoint = Column(String, nullable=False, unique=True, index=True)
    wallet_address = Column(String, unique=True, index=True)
    pricing_model = Column(String, default="free")
    price_per_call = Column(Float, default=0.0)
    capabilities = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)
    health_status = Column(String, default="unknown")
    trust_score = Column(Float, default=0.0)
