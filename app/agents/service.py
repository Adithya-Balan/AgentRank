from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.agents.models import Agent
from app.agents.schemas import AgentCreate, AgentUpdate


def list_agents(
    db: Session,
    *,
    category: str | None = None,
    is_active: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Agent]:
    query = select(Agent).order_by(Agent.trust_score.desc(), Agent.name.asc())

    if category is not None:
        query = query.where(Agent.category == category)

    if is_active is not None:
        query = query.where(Agent.is_active == is_active)

    return list(db.scalars(query.offset(offset).limit(limit)).all())


def get_agent(db: Session, agent_id: int) -> Agent | None:
    return db.get(Agent, agent_id)


def create_agent(db: Session, payload: AgentCreate) -> Agent:
    agent = Agent(**payload.model_dump())
    db.add(agent)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(agent)
    return agent


def update_agent(db: Session, agent: Agent, payload: AgentUpdate) -> Agent:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(agent, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(agent)
    return agent
