import logging
from sqlalchemy import Engine
from app.trust_scoring.models import TrustProfile, DomainTrust

logger = logging.getLogger(__name__)

def sync_trust_scoring_schema(engine: Engine):
    logger.info("Syncing Trust Scoring Schema...")
    TrustProfile.metadata.create_all(bind=engine)
    DomainTrust.metadata.create_all(bind=engine)
