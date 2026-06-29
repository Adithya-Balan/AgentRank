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
        
        if query:
            q = query.lower()
            filtered = [a for a in all_agents if q in a.name.lower() or q in a.category.lower() or any(q in cap.lower() for cap in a.capabilities)]
            
            # Hackathon Demo Magic: If no hardcoded agents match, dynamically "discover" one from the internet!
            if not filtered:
                import re
                # Extract potential price from query (e.g. "$0.01")
                price = 0.05
                price_match = re.search(r'\$?(\d+\.\d+)', query)
                if price_match:
                    price = float(price_match.group(1))
                    
                dynamic_agent = AgentCreate(
                    name=f"Crew_{query.split()[0].capitalize()}Agent",
                    category="Custom",
                    framework="CrewAI",
                    endpoint=f"https://api.crewai.example.com/agents/dynamic_{random.randint(100,999)}",
                    pricing_model="pay_per_call",
                    price_per_call=price,
                    capabilities=["dynamic_task", query[:20]],
                    staked_tokens=100.0,
                    wallet_address=f"0xCrew{random.randint(1000,9999)}"
                )
                return [dynamic_agent]
            return filtered
            
        return all_agents
