import logging
from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.agents.models import Agent
from app.agents.service import create_agent

from app.discovery.adapters.croo_store import CrooStoreAdapter
from app.discovery.models import SynchronizationLog, RegistrySnapshot

logger = logging.getLogger(__name__)

ADAPTERS = [
    CrooStoreAdapter(),
]

def run_discovery_cycle(db: Session) -> dict:
    results = {
        "total_found": 0,
        "new_added": 0,
        "updated": 0,
        "removed": 0,
        "failed_crawls": 0,
        "sources_crawled": []
    }
    
    # We maintain a set of all endpoints found in this global cycle
    found_endpoints = set()
    
    for adapter in ADAPTERS:
        source_name = adapter.source_name
        logger.info(f"Starting discovery on source: {source_name}")
        
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
                
                # Deduplicate and sync programmatically
                existing_agent = db.query(Agent).filter(Agent.endpoint == agent_payload.endpoint).first()
                if existing_agent:
                    # Sync metadata
                    existing_agent.price_per_call = agent_payload.price_per_call
                    existing_agent.is_active = True
                    results["updated"] += 1
                else:
                    try:
                        create_agent(db, agent_payload)
                        results["new_added"] += 1
                    except Exception as e:
                        db.rollback()
                        logger.error(f"Failed to create agent: {e}")
            
            # Save Registry Snapshot
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

    # Stale agent detection (Active agents NOT found in the public CROO ecosystem sync)
    # They should be marked inactive so they stop being recommended, but we keep history.
    if results["sources_crawled"]:
        stale_agents = db.query(Agent).filter(
            Agent.is_active == True,
            Agent.endpoint.notin_(found_endpoints)
        ).all()
        
        for stale in stale_agents:
            stale.is_active = False
            results["removed"] += 1
            
        db.commit()

    return results
