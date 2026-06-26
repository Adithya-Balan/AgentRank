from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.rankings import service
from app.rankings.schemas import RankingResponse


router = APIRouter()

@router.get("/recommend", response_model=RankingResponse)
def recommend_agents(
    category: str | None = Query(None, description="Filter by agent category"),
    capability: str | None = Query(None, description="Filter by a specific capability (e.g. 'citation-validation')"),
    max_price: float | None = Query(None, description="Maximum price per call"),
    min_trust_score: float | None = Query(None, description="Minimum overall trust score"),
    sort_by: str = Query("trust_score", description="Sort by: trust_score, price, or reliability"),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Query the AgentRank intelligence layer to find the best agents for specific tasks.
    Example: Find the most reliable research agent under $0.01.
    """
    return service.get_ranked_agents(
        db,
        category=category,
        capability=capability,
        max_price=max_price,
        min_trust_score=min_trust_score,
        sort_by=sort_by,
        limit=limit,
        offset=offset
    )
