from abc import ABC, abstractmethod
from app.agents.schemas import AgentCreate

class DiscoveryAdapter(ABC):
    """
    Base class for discovering agents across fragmented ecosystems.
    """
    @property
    @abstractmethod
    def source_name(self) -> str:
        pass

    @abstractmethod
    def crawl(self) -> list[AgentCreate]:
        """
        Connects to an external registry, API, or scrapes known endpoints
        to return a list of standard AgentCreate payloads.
        """
        pass
