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


def recompute_trust_score(db: Session, agent: Agent) -> dict:
    stats = db.execute(
        select(
            func.count(BenchmarkResult.id),
            func.avg(BenchmarkResult.score),
        ).where(BenchmarkResult.agent_id == agent.id)
    ).one()
    benchmark_count = int(stats[0] or 0)
    average_benchmark_score = float(stats[1]) if stats[1] is not None else None
    health_score = HEALTH_SCORE.get(agent.health_status or "unknown", 50.0)

    if average_benchmark_score is None:
        trust_score = health_score * 0.2
    else:
        trust_score = (0.8 * average_benchmark_score) + (0.2 * health_score)

    agent.trust_score = round(max(0.0, min(100.0, trust_score)), 2)

    return {
        "agent_id": agent.id,
        "trust_score": agent.trust_score,
        "benchmark_count": benchmark_count,
        "average_benchmark_score": (
            round(average_benchmark_score, 2)
            if average_benchmark_score is not None
            else None
        ),
        "health_status": agent.health_status or "unknown",
        "health_score": health_score,
        "formula": TRUST_FORMULA,
    }

