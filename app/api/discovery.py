from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.discovery import service

router = APIRouter()

@router.post("/sync", status_code=status.HTTP_200_OK)
def sync_croo_registry(db: Session = Depends(get_db)):
    """
    Force a live synchronization with the CROO Agent Store.
    Scrapes agent.croo.network, normalizes metadata, and upserts
    the PostgreSQL registry cache. Detects stale/removed agents.
    """
    return service.run_discovery_cycle(db)


@router.get("/status", status_code=status.HTTP_200_OK)
def get_cache_status(db: Session = Depends(get_db)):
    """
    Check whether the local CROO registry cache is fresh or stale.
    Useful for monitoring and debugging sync health.
    """
    fresh = service.is_cache_fresh(db)
    
    last_sync = db.query(service.SynchronizationLog).filter(
        service.SynchronizationLog.status == "success"
    ).order_by(service.SynchronizationLog.completed_at.desc()).first()
    
    return {
        "cache_fresh": fresh,
        "cache_ttl_minutes": service.CACHE_TTL_MINUTES,
        "last_successful_sync": last_sync.completed_at.isoformat() if last_sync and last_sync.completed_at else None,
        "agents_in_last_sync": last_sync.agents_found if last_sync else 0,
    }
