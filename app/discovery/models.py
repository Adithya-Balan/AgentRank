from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base

class SynchronizationLog(Base):
    __tablename__ = "synchronization_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, index=True, nullable=False)
    status = Column(String, nullable=False) # "success", "failed"
    agents_found = Column(Integer, default=0)
    agents_added = Column(Integer, default=0)
    agents_updated = Column(Integer, default=0)
    agents_removed = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String, nullable=True)

class RegistrySnapshot(Base):
    __tablename__ = "registry_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    sync_id = Column(Integer, ForeignKey("synchronization_logs.id"))
    snapshot_data = Column(JSON, nullable=False) # The full normalized state
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    sync_log = relationship("SynchronizationLog")
