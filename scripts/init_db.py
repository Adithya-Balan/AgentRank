from app.db.database import engine
from app.agents.schema_sync import sync_agent_registry_schema

sync_agent_registry_schema(engine)

print("Database initialized")
