import logging
import re
import json
import httpx
from bs4 import BeautifulSoup
from typing import List
from app.discovery.adapters.base import DiscoveryAdapter
from app.agents.schemas import AgentCreate

logger = logging.getLogger(__name__)

CROO_STORE_URL = "https://agent.croo.network"
CROO_API_BASE = "https://api.croo.network/backend/v1"


class CrooStoreAdapter(DiscoveryAdapter):
    """
    Discovers agents from the official CROO Agent Store.
    
    Uses a two-tier strategy:
    
    Tier 1 (Authenticated): If a CROO bearer token is configured via
            CROO_BEARER_TOKEN env var, hits the real CROO backend API
            at /backend/v1/me/agents for structured JSON data.
    
    Tier 2 (Public Scraping): Falls back to parsing the public HTML 
            at agent.croo.network for any agent metadata visible 
            without authentication.
    
    Returns ONLY real data extracted from the live CROO ecosystem.
    Returns an empty list if no agents can be discovered.
    """
    
    @property
    def source_name(self) -> str:
        return "croo_agent_store"
        
    def crawl(self) -> List[AgentCreate]:
        import os
        token = os.getenv("CROO_BEARER_TOKEN")
        
        all_agents = {}
        
        if token:
            logger.info("CROO bearer token found. Fetching user's private agents via API.")
            user_agents = self._discover_via_api(token)
            for a in user_agents:
                all_agents[a.endpoint] = a
                
        logger.info(f"Fetching public agents from CROO API...")
        public_agents = self._discover_via_scraping()
        
        for a in public_agents:
            # Overwrite if exists, or add new
            all_agents[a.endpoint] = a
            
        return list(all_agents.values())
    
    # ── Tier 1: Authenticated CROO Backend API ──────────────────────
    
    def _discover_via_api(self, token: str) -> List[AgentCreate]:
        """
        Query the real CROO backend API using an OAuth bearer token.
        Endpoint documented at: https://agent.croo.network/for-agents
        """
        agents = []
        
        try:
            response = httpx.get(
                f"{CROO_API_BASE}/me/agents",
                headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()
            
            # Normalize the API response into AgentCreate payloads
            agent_list = data if isinstance(data, list) else data.get("agents", data.get("data", []))
            
            for item in agent_list:
                if not isinstance(item, dict):
                    continue
                    
                name = item.get("name", "").strip()
                if not name:
                    continue
                    
                # Extract capabilities from skill tags
                capabilities = []
                for tag in item.get("skillTags", item.get("skills", [])):
                    if isinstance(tag, str):
                        capabilities.append(tag.lower().replace(" ", "_"))
                    elif isinstance(tag, dict):
                        capabilities.append(tag.get("name", "").lower().replace(" ", "_"))
                
                # Extract pricing from services
                price = 0.0
                services = item.get("services", [])
                if services and isinstance(services, list):
                    first_service = services[0]
                    if isinstance(first_service, dict):
                        # CROO stores prices in USDC micro units (6 decimals)
                        raw_price = first_service.get("price", 0)
                        price = float(raw_price) / 1_000_000 if raw_price > 1000 else float(raw_price)
                
                # Extract wallet address
                wallet = item.get("walletAddress", item.get("aaWalletAddress"))
                
                # Build deterministic endpoint from agent ID
                agent_id = item.get("id", item.get("agentId", name.lower()))
                
                agents.append(AgentCreate(
                    name=name.replace(" ", "_")[:120],
                    description=item.get("description"),
                    category=item.get("category", "CROO_Marketplace"),
                    framework="CAP",
                    endpoint=f"croo://api/{agent_id}",
                    wallet_address=wallet,
                    pricing_model="pay_per_call",
                    price_per_call=price,
                    capabilities=capabilities if capabilities else ["croo_service"],
                    staked_tokens=0.0
                ))
                
            logger.info(f"API discovery found {len(agents)} agents.")
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error("CROO bearer token expired or invalid. Re-authenticate via OAuth.")
            else:
                logger.error(f"CROO API error: {e}")
        except Exception as e:
            logger.error(f"CROO API discovery failed: {e}")
            
        return agents
    
    # ── Tier 2: Public HTML Scraping ────────────────────────────────
    
    def _discover_via_scraping(self) -> List[AgentCreate]:
        """
        Uses the undocumented public CROO API to discover agents without requiring
        an OAuth Bearer token. This is the new primary discovery mechanism for
        environments where a token isn't configured.
        """
        agents = []
        
        try:
            # We found this endpoint hidden in the Next.js bundle!
            public_api = f"{CROO_API_BASE}/public/agents"
            logger.info(f"Hitting public CROO API at {public_api}")
            
            response = httpx.get(
                public_api,
                headers={"Accept": "application/json"},
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()
            
            agent_list = data if isinstance(data, list) else data.get("agents", data.get("data", []))
            
            for item in agent_list:
                if not isinstance(item, dict):
                    continue
                    
                name = item.get("name", "").strip()
                if not name:
                    continue
                    
                capabilities = []
                for tag in item.get("skillTagSlugs", item.get("skillTags", [])):
                    if isinstance(tag, str):
                        capabilities.append(tag.lower().replace(" ", "_").replace("-", "_"))
                        
                price = 0.0
                raw_price = item.get("minServicePrice", 0)
                if raw_price:
                    # CROO stores prices in USDC micro units (6 decimals)
                    price = float(raw_price) / 1_000_000
                
                agent_id = item.get("agentId", name.lower())
                
                agents.append(AgentCreate(
                    name=name.replace(" ", "_")[:120],
                    description=item.get("description"),
                    category="CROO_Marketplace",
                    framework="CAP",
                    endpoint=f"croo://public_api/{agent_id}",
                    pricing_model="pay_per_call",
                    price_per_call=price,
                    capabilities=capabilities if capabilities else ["croo_service"],
                    staked_tokens=0.0
                ))
                
        except Exception as e:
            logger.error(f"Public API discovery failed: {e}")
        
        logger.info(f"Public discovery found {len(agents)} agents.")
        return agents
