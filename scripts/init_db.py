from app.db.database import engine
from app.agents.schema_sync import sync_agent_registry_schema
from app.evaluations.schema_sync import sync_benchmark_schema

sync_agent_registry_schema(engine)
sync_benchmark_schema(engine)

print("Database initialized")
