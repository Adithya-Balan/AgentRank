from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agents.schema_sync import sync_agent_registry_schema
from app.api import agents, validations, reputation, rankings, marketplace, discovery
from app.db.database import engine
from app.evaluations.schema_sync import sync_benchmark_schema
from app.validations.schema_sync import sync_validation_schema
from app.trust_scoring.schema_sync import sync_trust_scoring_schema
from app.reputation.schema_sync import sync_reputation_schema
from app.discovery.schema_sync import sync_discovery_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    sync_agent_registry_schema(engine)
    sync_benchmark_schema(engine)
    sync_validation_schema(engine)
    sync_trust_scoring_schema(engine)
    sync_reputation_schema(engine)
    sync_discovery_schema(engine)
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

app.include_router(
    reputation.router,
    prefix="/reputation",
    tags=["Reputation"],
)

app.include_router(
    rankings.router,
    prefix="/rankings",
    tags=["Rankings"],
)

app.include_router(
    marketplace.router,
    prefix="/marketplace",
    tags=["Marketplace"],
)

app.include_router(
    discovery.router,
    prefix="/discovery",
    tags=["Discovery"],
)
