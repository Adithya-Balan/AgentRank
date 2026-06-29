from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.agents.models import Agent
from app.evaluations.models import BenchmarkResult
from app.evaluations.schemas import BenchmarkResultCreate


HEALTH_SCORE = {
    "healthy": 100.0,
    "degraded": 60.0,
    "unknown": 50.0,
    "invalid_endpoint": 20.0,
    "unreachable": 0.0,
}

TRUST_FORMULA = "0.80 * average_benchmark_score + 0.20 * health_score"


def list_benchmark_results(
    db: Session,
    *,
    agent_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[BenchmarkResult]:
    query = (
        select(BenchmarkResult)
        .where(BenchmarkResult.agent_id == agent_id)
        .order_by(BenchmarkResult.created_at.desc(), BenchmarkResult.id.desc())
    )
    return list(db.scalars(query.offset(offset).limit(limit)).all())


def create_benchmark_result(
    db: Session,
    *,
    agent: Agent,
    payload: BenchmarkResultCreate,
) -> BenchmarkResult:
    result = BenchmarkResult(
        agent_id=agent.id,
        **payload.model_dump(),
    )
    db.add(result)
    db.flush()
    recompute_trust_score(db, agent)
    db.commit()
    db.refresh(result)
    db.refresh(agent)
    return result


def recompute_trust_score(db: Session, agent: Agent):
    from app.trust_scoring.service import compute_agent_trust_profile
    return compute_agent_trust_profile(db, agent.id)

