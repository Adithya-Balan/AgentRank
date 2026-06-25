from fastapi import FastAPI
from app.api import agents

app = FastAPI()

app.include_router(
    agents.router,
    prefix="/agents",
    tags=["Agents"]
)