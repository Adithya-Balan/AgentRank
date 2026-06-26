import logging
from sqlalchemy import Engine
from app.validations.models import ValidationReport

logger = logging.getLogger(__name__)

def sync_validation_schema(engine: Engine):
    logger.info("Syncing Validation Schema...")
    ValidationReport.metadata.create_all(bind=engine)
