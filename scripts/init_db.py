"""
Database initialization and reset utility for AgentRank.
Drops all tables and recreates them, then triggers a live CROO sync.

Usage:
    PYTHONPATH=. uv run python scripts/init_db.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import engine, SessionLocal, Base

# Import all models so SQLAlchemy knows about them
from app.agents.models import Agent
from app.evaluations.models import BenchmarkResult
from app.validations.models import ValidationReport
from app.trust_scoring.models import TrustProfile, DomainTrust
from app.reputation.models import AgentInteraction
from app.discovery.models import SynchronizationLog, RegistrySnapshot

def init():
    from sqlalchemy import text
    
    print("Dropping all existing tables (CASCADE)...")
    with engine.connect() as conn:
        # Get all table names and drop with CASCADE to handle FK dependencies
        result = conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        ))
        tables = [row[0] for row in result]
        for table in tables:
            conn.execute(text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
        conn.commit()
    
    print("Creating all tables from scratch...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database initialized with clean schema.")
    print("   No mock data seeded. Run POST /discovery/sync to populate from live CROO Store.")

if __name__ == "__main__":
    init()
