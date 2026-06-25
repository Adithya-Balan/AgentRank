from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agents.schema_sync import sync_agent_registry_schema
from app.api import agents
from app.db.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    sync_agent_registry_schema(engine)
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
