import random
from app.discovery.adapters.base import DiscoveryAdapter
from app.agents.schemas import AgentCreate

class CrewAIAdapter(DiscoveryAdapter):
    @property
    def source_name(self):
        return "crewai_hub"
        
    def crawl(self) -> list[AgentCreate]:
        # Simulate hitting a CrewAI enterprise hub or public registry
        # We assign a random wallet for simulation purposes
        return [
            AgentCreate(
                name="Crew_SeniorResearcher",
                category="Research",
                framework="CrewAI",
                endpoint="https://api.crewai.example.com/agents/researcher",
                wallet_address=f"0xCrew{random.randint(1000,9999)}",
                pricing_model="pay_per_call",
                price_per_call=0.02,
                capabilities=["deep_research", "summarization"],
                staked_tokens=150.0  # Enterprise staked agents
            ),
            AgentCreate(
                name="Crew_DataAnalyst",
                category="Analysis",
                framework="CrewAI",
                endpoint="https://api.crewai.example.com/agents/analyst",
                wallet_address=f"0xCrew{random.randint(1000,9999)}",
                pricing_model="pay_per_call",
                price_per_call=0.05,
                capabilities=["data_analysis", "python_execution"],
                staked_tokens=500.0
            )
        ]
