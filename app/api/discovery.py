from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.discovery import service

router = APIRouter()

@router.post("/run", status_code=status.HTTP_200_OK)
def run_agent_discovery(db: Session = Depends(get_db)):
    """
    Trigger the CROO-native agent discovery pipeline.
    Scrapes the official CROO Agent Store to discover new CAP-compatible 
    autonomous agents, syncing metadata into the PostgreSQL cache.
    """
    return service.run_discovery_cycle(db)
