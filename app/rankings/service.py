from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, asc, cast, String

from app.agents.models import Agent
from app.trust_scoring.models import TrustProfile
from app.rankings.schemas import RankedAgent, RankingResponse
from app.discovery.service import ensure_fresh_cache


def get_ranked_agents(
    db: Session,
    category: str | None = None,
    capability: str | None = None,
    max_price: float | None = None,
    min_trust_score: float | None = None,
    sort_by: str = "trust_score",
    limit: int = 10,
    offset: int = 0
) -> RankingResponse:
    # Ensure the CROO registry cache is fresh before querying
    ensure_fresh_cache(db)
    
    query = select(Agent, TrustProfile).outerjoin(
        TrustProfile, Agent.id == TrustProfile.agent_id
    ).where(Agent.is_active == True)

    if category:
        query = query.where(Agent.category == category)
        
    if capability:
        # Cross-DB hack for basic JSON array searching
        query = query.where(cast(Agent.capabilities, String).like(f'%{capability}%'))

    if max_price is not None:
        query = query.where(Agent.price_per_call <= max_price)
        
    if min_trust_score is not None:
        query = query.where(Agent.trust_score >= min_trust_score)

    # Sorting
    if sort_by == "price":
        query = query.order_by(asc(Agent.price_per_call), desc(Agent.trust_score))
    elif sort_by == "reliability":
        query = query.order_by(desc(TrustProfile.reliability_score), desc(Agent.trust_score))
    else:  # default is trust_score
        query = query.order_by(desc(Agent.trust_score), asc(Agent.price_per_call))

    # Calculate total matching before applying offset/limit
    count_query = select(func.count()).select_from(query.subquery())
    total_found = db.execute(count_query).scalar() or 0

    results = db.execute(query.offset(offset).limit(limit)).all()
    
    ranked_agents = []
    for agent, profile in results:
        ranked_agents.append(RankedAgent(
            agent_id=agent.id,
            name=agent.name,
            category=agent.category,
            price_per_call=agent.price_per_call,
            overall_trust_score=agent.trust_score,
            reliability_score=profile.reliability_score if profile else None,
            latency_score=profile.latency_score if profile else None,
            health_status=agent.health_status,
            capabilities=agent.capabilities if agent.capabilities else [],
        ))

    return RankingResponse(results=ranked_agents, total_found=total_found)
