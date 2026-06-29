import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.agents.models import Agent
from app.agents.service import create_agent

from app.discovery.adapters.croo_store import CrooStoreAdapter
from app.discovery.models import SynchronizationLog, RegistrySnapshot

logger = logging.getLogger(__name__)

# Cache freshness configuration
CACHE_TTL_MINUTES = 30  # How long before we consider the registry stale

ADAPTERS = [
    CrooStoreAdapter(),
]


def is_cache_fresh(db: Session) -> bool:
    """
    Check if the PostgreSQL registry cache is still fresh.
    Returns True if the last successful sync was within CACHE_TTL_MINUTES.
    """
    last_sync = db.query(SynchronizationLog).filter(
        SynchronizationLog.status == "success"
    ).order_by(SynchronizationLog.completed_at.desc()).first()
    
    if not last_sync or not last_sync.completed_at:
        return False
    
    age = datetime.now(timezone.utc) - last_sync.completed_at
    return age < timedelta(minutes=CACHE_TTL_MINUTES)


def ensure_fresh_cache(db: Session) -> dict | None:
    """
    Called by downstream services (rankings, marketplace) before querying.
    If the cache is stale, triggers a live scrape. If fresh, returns None (no-op).
    """
    if is_cache_fresh(db):
        logger.info("Registry cache is fresh. Skipping live scrape.")
        return None
    
    logger.info("Registry cache is stale. Triggering live CROO scrape...")
    return run_discovery_cycle(db)


def run_discovery_cycle(db: Session) -> dict:
    """
    Execute the full CROO-native discovery pipeline:
    1. Scrape agent.croo.network
    2. Normalize discovered metadata
    3. Upsert into PostgreSQL registry cache
    4. Detect and mark stale/removed agents
    5. Save sync audit log and registry snapshot
    """
    results = {
        "total_found": 0,
        "new_added": 0,
        "updated": 0,
        "removed": 0,
        "failed_crawls": 0,
        "sources_crawled": [],
        "cache_was_stale": True
    }
    
    found_endpoints = set()
    
    for adapter in ADAPTERS:
        source_name = adapter.source_name
        logger.info(f"Starting live discovery on source: {source_name}")
        
        sync_log = SynchronizationLog(source_name=source_name, status="running")
        db.add(sync_log)
        db.commit()
        db.refresh(sync_log)
        
        try:
            agents_payload = adapter.crawl()
            results["sources_crawled"].append(source_name)
            results["total_found"] += len(agents_payload)
            
            snapshot_data = []
            
            for agent_payload in agents_payload:
                found_endpoints.add(agent_payload.endpoint)
                snapshot_data.append(agent_payload.model_dump())
                
                # Upsert: update existing or create new
                existing_agent = db.query(Agent).filter(
                    Agent.endpoint == agent_payload.endpoint
                ).first()
                
                if existing_agent:
                    # Refresh volatile metadata from live source
                    existing_agent.name = agent_payload.name
                    existing_agent.price_per_call = agent_payload.price_per_call
                    existing_agent.capabilities = agent_payload.capabilities
                    existing_agent.description = agent_payload.description
                    existing_agent.is_active = True
                    results["updated"] += 1
                else:
                    try:
                        create_agent(db, agent_payload)
                        results["new_added"] += 1
                    except Exception as e:
                        db.rollback()
                        logger.error(f"Failed to create agent: {e}")
            
            # Save Registry Snapshot for audit trail
            snapshot = RegistrySnapshot(
                sync_id=sync_log.id,
                snapshot_data=snapshot_data
            )
            db.add(snapshot)
            
            sync_log.status = "success"
            sync_log.completed_at = datetime.now(timezone.utc)
            sync_log.agents_found = len(agents_payload)
            sync_log.agents_added = results["new_added"]
            sync_log.agents_updated = results["updated"]
            
        except Exception as e:
            logger.error(f"Failed to crawl {source_name}: {e}")
            sync_log.status = "failed"
            sync_log.error_message = str(e)
            sync_log.completed_at = datetime.now(timezone.utc)
            results["failed_crawls"] += 1
            
        db.commit()

    # Stale agent detection:
    # Agents in our cache that are NO LONGER found on the live CROO Store
    # are marked inactive so they stop appearing in recommendations.
    # Their trust history and reputation data are preserved.
    if found_endpoints:
        stale_agents = db.query(Agent).filter(
            Agent.is_active == True,
            Agent.endpoint.like("croo://%"),  # Only touch CROO-sourced agents
            Agent.endpoint.notin_(found_endpoints)
        ).all()
        
        for stale in stale_agents:
            stale.is_active = False
            results["removed"] += 1
            
        db.commit()

    return results
