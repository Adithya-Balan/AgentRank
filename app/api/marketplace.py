from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.marketplace import service
from app.marketplace.schemas import RoutingRequest, RoutingResponse


router = APIRouter()

@router.post("/route", response_model=RoutingResponse)
def autonomous_agent_routing(
    payload: RoutingRequest,
    db: Session = Depends(get_db)
):
    """
    Simulates autonomous agent orchestration over the CAP protocol.
    Given a list of tasks and a budget, AgentRank routes the work 
    to the highest-trusted affordable agents, records the interaction 
    in the reputation graph, and simulates the transaction.
    """
    return service.execute_autonomous_routing(db, payload)
