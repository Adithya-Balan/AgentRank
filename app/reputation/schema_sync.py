import logging
from sqlalchemy import Engine
from app.reputation.models import AgentInteraction

logger = logging.getLogger(__name__)

def sync_reputation_schema(engine: Engine):
    logger.info("Syncing Reputation Schema...")
    AgentInteraction.metadata.create_all(bind=engine)
