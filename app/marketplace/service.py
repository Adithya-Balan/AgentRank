from sqlalchemy.orm import Session
from fastapi import HTTPException
import uuid

from app.rankings.service import get_ranked_agents
from app.reputation.service import log_interaction
from app.reputation.schemas import AgentInteractionCreate
from app.marketplace.schemas import RoutingRequest, RoutingResponse, HiredAgentDetails


def execute_autonomous_routing(db: Session, request: RoutingRequest) -> RoutingResponse:
    # Cache freshness is handled by get_ranked_agents() downstream
    budget_remaining = request.max_budget
    total_cost = 0.0
    hired_agents = []
    
    for task in request.tasks:
        ranking = get_ranked_agents(
            db=db,
            capability=task.required_capability,
            max_price=budget_remaining, # Can't exceed remaining budget for a single task
            sort_by="trust_score",
            limit=1
        )
        
        if not ranking.results:
            raise HTTPException(
                status_code=404,
                detail=f"No affordable/trusted agent found for capability: {task.required_capability}"
            )
            
        best_agent = ranking.results[0]
        
        # Deduct cost
        budget_remaining -= best_agent.price_per_call
        total_cost += best_agent.price_per_call
        
        # Simulate CAP transaction
        transaction_id = f"cap_tx_{uuid.uuid4().hex[:12]}"
        
        # Log Reputation Interaction
        interaction_payload = AgentInteractionCreate(
            source_agent_id=request.source_agent_id,
            target_agent_id=best_agent.agent_id,
            interaction_type="autonomous_hire",
            success=True,
            task_description=task.task_name,
            cost_incurred=best_agent.price_per_call,
            latency_ms=250.0  # Simulated latency for execution
        )
        
        interaction = log_interaction(db, interaction_payload)
        
        hired_agents.append(HiredAgentDetails(
            task_name=task.task_name,
            agent_id=best_agent.agent_id,
            agent_name=best_agent.name,
            price_paid=best_agent.price_per_call,
            transaction_id=transaction_id,
            interaction_id=interaction.id
        ))
        
    return RoutingResponse(
        source_agent_id=request.source_agent_id,
        total_cost=round(total_cost, 4),
        budget_remaining=round(budget_remaining, 4),
        hired_agents=hired_agents,
        status="orchestration_complete"
    )
