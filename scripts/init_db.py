from app.db.database import engine
from app.models.agent import Agent
from app.db.database import Base

Base.metadata.create_all(bind=engine)

print("Database initialized")