from pydantic import BaseModel

class RoutingTask(BaseModel):
    task_name: str
    required_capability: str

class RoutingRequest(BaseModel):
    source_agent_id: int
    tasks: list[RoutingTask]
    max_budget: float

class HiredAgentDetails(BaseModel):
    task_name: str
    agent_id: int
    agent_name: str
    price_paid: float
    transaction_id: str
    interaction_id: int

class RoutingResponse(BaseModel):
    source_agent_id: int
    total_cost: float
    budget_remaining: float
    hired_agents: list[HiredAgentDetails]
    status: str
