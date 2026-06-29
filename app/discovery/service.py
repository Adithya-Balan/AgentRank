import logging
from sqlalchemy.orm import Session
from app.agents.models import Agent
from app.agents.service import create_agent

from app.discovery.adapters.mcp import MCPAdapter
from app.discovery.adapters.crewai import CrewAIAdapter

logger = logging.getLogger(__name__)

ADAPTERS = [
    MCPAdapter(),
    CrewAIAdapter(),
]

def run_discovery_cycle(db: Session) -> dict:
    results = {
        "total_found": 0,
        "new_added": 0,
        "failed_crawls": 0,
        "sources_crawled": []
    }
    
    for adapter in ADAPTERS:
        source_name = adapter.source_name
        logger.info(f"Starting discovery on source: {source_name}")
        
        try:
            agents = adapter.crawl()
            results["sources_crawled"].append(source_name)
            results["total_found"] += len(agents)
            
            for agent_payload in agents:
                # Deduplicate programmatically
                existing_agent = db.query(Agent).filter(Agent.endpoint == agent_payload.endpoint).first()
                if existing_agent:
                    continue
                    
                try:
                    create_agent(db, agent_payload)
                    results["new_added"] += 1
                except Exception as e:
                    # Catch any other DB errors
                    db.rollback()
        except Exception as e:
            logger.error(f"Failed to crawl {source_name}: {e}")
            results["failed_crawls"] += 1
            
    return results
