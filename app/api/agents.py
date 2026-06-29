from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.agents import service
from app.agents.schemas import (
    AgentCreate,
    AgentHealthCheckRead,
    AgentRead,
    AgentUpdate,
)
from app.db.database import get_db
from app.evaluations import service as evaluation_service
from app.evaluations.schemas import (
    BenchmarkResultCreate,
    BenchmarkResultRead,
)
from app.trust_scoring.schemas import TrustProfileRead
from app.trust_scoring.service import compute_agent_trust_profile, get_trust_profile_with_decay

router = APIRouter()


@router.get("/", response_model=list[AgentRead])
def get_agents(
    category: str | None = None,
    is_active: bool | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return service.list_agents(
        db,
        category=category,
        is_active=is_active,
        limit=limit,
        offset=offset,
    )


@router.post("/", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
def create_agent(payload: AgentCreate, db: Session = Depends(get_db)):
    try:
        return service.create_agent(db, payload)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Agent endpoint or wallet address is already registered.",
        ) from exc


@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = service.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found.",
        )

    return agent


@router.patch("/{agent_id}", response_model=AgentRead)
def update_agent(
    agent_id: int,
    payload: AgentUpdate,
    db: Session = Depends(get_db),
):
    agent = service.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found.",
        )

    try:
        return service.update_agent(db, agent, payload)
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Agent endpoint or wallet address is already registered.",
        ) from exc


@router.post("/{agent_id}/health-check", response_model=AgentHealthCheckRead)
def run_agent_health_check(
    agent_id: int,
    timeout_seconds: float = Query(default=5.0, ge=0.1, le=30.0),
    db: Session = Depends(get_db),
):
    agent = service.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found.",
        )

    result = service.run_health_check(
        db,
        agent,
        timeout_seconds=timeout_seconds,
    )
    return {
        "agent_id": agent.id,
        "endpoint": agent.endpoint,
        "status": result.status,
        "status_code": result.status_code,
        "response_time_ms": result.response_time_ms,
        "error": result.error,
        "checked_at": result.checked_at,
    }


@router.get("/{agent_id}/benchmarks", response_model=list[BenchmarkResultRead])
def get_agent_benchmarks(
    agent_id: int,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    agent = service.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found.",
        )

    return evaluation_service.list_benchmark_results(
        db,
        agent_id=agent.id,
        limit=limit,
        offset=offset,
    )


@router.post(
    "/{agent_id}/benchmarks",
    response_model=BenchmarkResultRead,
    status_code=status.HTTP_201_CREATED,
)
def create_agent_benchmark(
    agent_id: int,
    payload: BenchmarkResultCreate,
    db: Session = Depends(get_db),
):
    agent = service.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found.",
        )

    return evaluation_service.create_benchmark_result(
        db,
        agent=agent,
        payload=payload,
    )


@router.post(
    "/{agent_id}/trust-score/recompute",
    response_model=TrustProfileRead,
)
def recompute_agent_trust_score(
    agent_id: int,
    db: Session = Depends(get_db),
):
    agent = service.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found.",
        )

    profile = compute_agent_trust_profile(db, agent.id)
    return profile


@router.get(
    "/{agent_id}/trust-profile",
    response_model=TrustProfileRead,
)
def get_agent_trust_profile(
    agent_id: int,
    db: Session = Depends(get_db),
):
    agent = service.get_agent(db, agent_id)
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found.",
        )
    profile = get_trust_profile_with_decay(db, agent_id)
    
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trust profile not found.",
        )
    return profile
