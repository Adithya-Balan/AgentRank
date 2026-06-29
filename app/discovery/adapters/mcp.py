from app.discovery.adapters.base import DiscoveryAdapter
from app.agents.schemas import AgentCreate

class MCPAdapter(DiscoveryAdapter):
    @property
    def source_name(self):
        return "mcp_registry"
        
    def crawl(self) -> list[AgentCreate]:
        # Simulate crawling an MCP (Model Context Protocol) manifest or local broadcast
        return [
            AgentCreate(
                name="MCP_FileSearcher",
                category="Utilities",
                framework="MCP",
                endpoint="mcp://local/filesearch",
                pricing_model="free",
                price_per_call=0.0,
                capabilities=["file_system_read", "search"],
                staked_tokens=0.0
            ),
            AgentCreate(
                name="MCP_PostgresConnector",
                category="Database",
                framework="MCP",
                endpoint="mcp://local/postgres",
                pricing_model="free",
                price_per_call=0.0,
                capabilities=["sql_query", "db_introspection"],
                staked_tokens=0.0
            )
        ]
