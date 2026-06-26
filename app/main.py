from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agents.schema_sync import sync_agent_registry_schema
from app.api import agents, validations
from app.db.database import engine
from app.evaluations.schema_sync import sync_benchmark_schema
from app.validations.schema_sync import sync_validation_schema
from app.trust_scoring.schema_sync import sync_trust_scoring_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    sync_agent_registry_schema(engine)
    sync_benchmark_schema(engine)
    sync_validation_schema(engine)
    sync_trust_scoring_schema(engine)
    yield


app = FastAPI(
    title="AgentRank",
    description="Trust, reputation, and evaluation infrastructure for AI agents.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(
    agents.router,
    prefix="/agents",
    tags=["Agents"],
)

app.include_router(
    validations.router,
    prefix="",
    tags=["Validations"],
)
