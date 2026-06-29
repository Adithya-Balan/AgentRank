from sqlalchemy import Engine

from app.discovery import models

def sync_discovery_schema(engine: Engine):
    """
    Creates discovery-related tables (SynchronizationLog, RegistrySnapshot) if they do not exist.
    """
    models.Base.metadata.create_all(bind=engine, tables=[
        models.SynchronizationLog.__table__,
        models.RegistrySnapshot.__table__
    ])
