from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    category = Column(String)

    endpoint = Column(String)

    wallet_address = Column(String)

    trust_score = Column(Float, default=0.0)