from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.discovery import service

router = APIRouter()

@router.post("/run", status_code=status.HTTP_200_OK)
def run_agent_discovery(db: Session = Depends(get_db)):
    """
    Trigger the hybrid agent discovery pipeline.
    Crawls registered adapters (MCP, CrewAI, LangChain, etc.) to discover
    new autonomous agents dynamically on the internet, solving the 
    universal opt-in registration problem.
    """
    return service.run_discovery_cycle(db)
