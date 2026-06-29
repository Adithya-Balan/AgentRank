from sqlalchemy.orm import Session
from sqlalchemy import select, func, cast, Integer

from app.agents.models import Agent
from app.reputation.models import AgentInteraction
from app.reputation.schemas import AgentInteractionCreate, ReputationGraph, ReputationGraphEdge


def log_interaction(db: Session, payload: AgentInteractionCreate) -> AgentInteraction:
    interaction = AgentInteraction(**payload.model_dump())
    db.add(interaction)
    
    # -------------------------------------------------------------
    # SIMULATE PROBABILISTIC EVALUATION (V2 Feature)
    # -------------------------------------------------------------
    # In V2, we don't evaluate every interaction. We fetch the agent's
    # uncertainty (sigma) and roll a die.
    from app.trust_scoring.service import get_trust_profile_with_decay
    profile = get_trust_profile_with_decay(db, payload.target_agent_id)
    
    # If the variance (sigma) is high, probability of audit is higher.
    # In a real system, we'd trigger an async Celery task here.
    # For MVP, we just log it.
    import random
    audit_triggered = False
    if profile and hasattr(profile, "domain_trusts") and profile.domain_trusts:
        # Get highest sigma
        max_sigma = max(dt.sigma for dt in profile.domain_trusts)
        # E.g., if sigma is 30, 30% chance to audit
        probability = min(max_sigma / 100.0, 1.0)
        if random.random() < probability:
            audit_triggered = True
            
    db.commit()
    db.refresh(interaction)
    # We can dynamically attach it for logs if we wanted, but not in DB schema yet
    setattr(interaction, "audit_triggered", audit_triggered)
    return interaction


def get_reputation_graph(db: Session, agent_id: int) -> ReputationGraph:
    agent = db.execute(select(Agent).where(Agent.id == agent_id)).scalar_one_or_none()
    if not agent:
        raise ValueError("Agent not found")
        
    # Outbound Dependencies (Who this agent hires)
    outbound_stats = db.execute(
        select(
            AgentInteraction.target_agent_id,
            Agent.name,
            func.count(AgentInteraction.id),
            func.avg(cast(AgentInteraction.success, Integer)),
            func.avg(AgentInteraction.latency_ms),
            Agent.trust_score
        )
        .join(Agent, Agent.id == AgentInteraction.target_agent_id)
        .where(AgentInteraction.source_agent_id == agent_id)
        .group_by(AgentInteraction.target_agent_id, Agent.name, Agent.trust_score)
    ).all()
    
    outbound_edges = []
    total_dependency_trust = 0.0
    dependency_count = 0
    
    for row in outbound_stats:
        target_id, target_name, count, success_rate, avg_latency, trust_score = row
        outbound_edges.append(ReputationGraphEdge(
            target_agent_id=target_id,
            target_agent_name=target_name,
            interaction_count=count,
            success_rate=float(success_rate or 0.0) * 100.0,
            average_latency_ms=float(avg_latency or 0.0)
        ))
        total_dependency_trust += (trust_score or 0.0)
        dependency_count += 1
        
    network_reliability_score = (total_dependency_trust / dependency_count) if dependency_count > 0 else 100.0
    
    # Inbound Dependents (Who hires this agent)
    inbound_stats = db.execute(
        select(
            AgentInteraction.source_agent_id,
            Agent.name,
            func.count(AgentInteraction.id),
            func.avg(cast(AgentInteraction.success, Integer)),
            func.avg(AgentInteraction.latency_ms),
            Agent.staked_tokens,
            Agent.trust_score
        )
        .join(Agent, Agent.id == AgentInteraction.source_agent_id)
        .where(AgentInteraction.target_agent_id == agent_id)
        .group_by(AgentInteraction.source_agent_id, Agent.name, Agent.staked_tokens, Agent.trust_score)
    ).all()
    
    inbound_edges = []
    total_eigen_weight = 0.0
    total_stake = 0.0
    
    for row in inbound_stats:
        source_id, source_name, count, success_rate, avg_latency, stake, trust = row
        success = float(success_rate or 0.0)
        inbound_edges.append(ReputationGraphEdge(
            target_agent_id=source_id,
            target_agent_name=source_name,
            interaction_count=count,
            success_rate=success * 100.0,
            average_latency_ms=float(avg_latency or 0.0)
        ))
        
        # Calculate Eigen-Reputation (Stake-weighted)
        effective_stake = float(stake or 0.0) + 1.0 # Baseline stake
        total_eigen_weight += effective_stake * float(trust or 0.0) * success
        total_stake += effective_stake
        
    eigen_reputation_score = (total_eigen_weight / total_stake) if total_stake > 0 else 0.0
        
    return ReputationGraph(
        agent_id=agent_id,
        agent_name=agent.name,
        outbound_dependencies=outbound_edges,
        inbound_dependents=inbound_edges,
        network_reliability_score=round(network_reliability_score, 2),
        eigen_reputation_score=round(eigen_reputation_score, 2)
    )
