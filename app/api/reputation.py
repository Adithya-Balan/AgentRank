from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.reputation import service
from app.reputation.schemas import AgentInteractionCreate, AgentInteractionRead, ReputationGraph


router = APIRouter()

@router.post(
    "/interactions",
    response_model=AgentInteractionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_interaction(
    payload: AgentInteractionCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.log_interaction(db, payload)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid source or target agent ID")


@router.get(
    "/{agent_id}/graph",
    response_model=ReputationGraph,
)
def get_agent_reputation_graph(
    agent_id: int,
    db: Session = Depends(get_db),
):
    try:
        return service.get_reputation_graph(db, agent_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
