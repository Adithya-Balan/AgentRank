from datetime import datetime, UTC
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.agents.models import Agent
from app.evaluations.models import BenchmarkResult
from app.validations.models import ValidationReport
from app.trust_scoring.models import TrustProfile, DomainTrust
from app.evaluations.service import HEALTH_SCORE


def compute_agent_trust_profile(db: Session, agent_id: int) -> TrustProfile:
    agent = db.execute(select(Agent).where(Agent.id == agent_id)).scalar_one_or_none()
    if not agent:
        raise ValueError("Agent not found")
        
    # Query aggregated validation metrics
    validation_stats = db.execute(
        select(
            func.avg(ValidationReport.factual_accuracy_score),
            func.avg(ValidationReport.citation_reliability_score),
            func.avg(ValidationReport.consistency_score),
            func.avg(ValidationReport.economic_efficiency_score),
            func.avg(ValidationReport.prompt_adherence_score),
            func.avg(ValidationReport.reasoning_quality_score),
            func.avg(ValidationReport.hallucination_rate),
        ).where(ValidationReport.agent_id == agent_id)
    ).one()
    
    avg_accuracy = float(validation_stats[0] or 0.0)
    avg_citation = float(validation_stats[1] or 0.0)
    avg_consistency = float(validation_stats[2] or 0.0)
    avg_economic = float(validation_stats[3] or 0.0)
    avg_adherence = float(validation_stats[4] or 0.0)
    avg_reasoning = float(validation_stats[5] or 0.0)
    avg_hallucination = float(validation_stats[6] or 0.0)
    
    # Accuracy heavily penalized by hallucination
    accuracy_score = max(0.0, avg_accuracy - avg_hallucination)
    
    # Query benchmark metrics for reliability & latency
    benchmark_stats = db.execute(
        select(
            func.avg(BenchmarkResult.latency_ms),
            func.count(BenchmarkResult.id),
        ).where(BenchmarkResult.agent_id == agent_id)
    ).one()
    
    avg_latency_ms = float(benchmark_stats[0] or 0.0)
    benchmark_count = int(benchmark_stats[1] or 0)
    
    # Calculate Reliability (depends on health score and passing benchmarks)
    health_score = HEALTH_SCORE.get(agent.health_status or "unknown", 50.0)
    
    passed_benchmarks = db.execute(
        select(func.count(BenchmarkResult.id))
        .where(BenchmarkResult.agent_id == agent_id, BenchmarkResult.passed == True)
    ).scalar() or 0
    
    pass_rate = (passed_benchmarks / benchmark_count * 100.0) if benchmark_count > 0 else 0.0
    reliability_score = (pass_rate * 0.5) + (health_score * 0.5)
    
    # Normalize latency (lower is better). Let's say <= 500ms is 100, >= 5000ms is 0
    if avg_latency_ms <= 500:
        latency_score = 100.0
    elif avg_latency_ms >= 5000:
        latency_score = 0.0
    else:
        latency_score = 100.0 - ((avg_latency_ms - 500) / 4500.0 * 100.0)
        
    # Consensus Alignment (combines prompt adherence and reasoning)
    consensus_alignment_score = (avg_adherence + avg_reasoning) / 2.0
    
    # Apply Weights
    # Accuracy (35%), Citation Quality (20%), Reliability (15%), Consistency (10%), Cost Efficiency (10%), Latency (5%), Consensus Alignment (5%)
    overall_trust_score = (
        (accuracy_score * 0.35) +
        (avg_citation * 0.20) +
        (reliability_score * 0.15) +
        (avg_consistency * 0.10) +
        (avg_economic * 0.10) +
        (latency_score * 0.05) +
        (consensus_alignment_score * 0.05)
    )
    
    overall_trust_score = round(max(0.0, min(100.0, overall_trust_score)), 2)
    
    # Update or create TrustProfile
    profile = db.execute(
        select(TrustProfile).where(TrustProfile.agent_id == agent_id)
    ).scalar_one_or_none()
    
    if not profile:
        profile = TrustProfile(agent_id=agent_id)
        db.add(profile)
        
    profile.accuracy_score = round(accuracy_score, 2)
    profile.citation_quality_score = round(avg_citation, 2)
    profile.reliability_score = round(reliability_score, 2)
    profile.consistency_score = round(avg_consistency, 2)
    profile.cost_efficiency_score = round(avg_economic, 2)
    profile.latency_score = round(latency_score, 2)
    profile.consensus_alignment_score = round(consensus_alignment_score, 2)
    profile.overall_trust_score = overall_trust_score
    
    # Update Agent trust score
    agent.trust_score = overall_trust_score
    
    # Update DomainTrust based on agent capabilities
    if agent.capabilities:
        for capability in agent.capabilities:
            domain_trust = db.execute(
                select(DomainTrust).where(DomainTrust.agent_id == agent_id, DomainTrust.domain == capability)
            ).scalar_one_or_none()
            
            if not domain_trust:
                domain_trust = DomainTrust(agent_id=agent_id, domain=capability)
                db.add(domain_trust)
            
            # Reset sigma (uncertainty) on fresh evaluation, mu tracks overall score for simplicity
            domain_trust.mu = overall_trust_score
            domain_trust.sigma = 5.0 # Low uncertainty after a fresh evaluation
            domain_trust.last_evaluated_at = datetime.now(UTC)

    db.commit()
    db.refresh(profile)
    return profile


def get_trust_profile_with_decay(db: Session, agent_id: int):
    profile = db.execute(
        select(TrustProfile).where(TrustProfile.agent_id == agent_id)
    ).scalar_one_or_none()
    
    if not profile:
        return None
        
    domain_trusts = db.execute(
        select(DomainTrust).where(DomainTrust.agent_id == agent_id)
    ).scalars().all()
    
    # Apply Trust Decay: Variance (sigma) increases linearly over time
    DECAY_RATE_PER_HOUR = 0.5 
    now = datetime.now(UTC)
    
    for dt in domain_trusts:
        # Time since last evaluation in hours
        # Make sure dt.last_evaluated_at is aware
        last_eval = dt.last_evaluated_at
        if last_eval.tzinfo is None:
            last_eval = last_eval.replace(tzinfo=UTC)
            
        hours_passed = (now - last_eval).total_seconds() / 3600.0
        # Decay sigma (uncertainty increases)
        dt.sigma = min(100.0, dt.sigma + (hours_passed * DECAY_RATE_PER_HOUR))
    
    db.commit()
    db.refresh(profile)
    
    # Convert to dict/schema to include domain_trusts
    # Fast approach: set it dynamically
    setattr(profile, "domain_trusts", domain_trusts)
    
    return profile
