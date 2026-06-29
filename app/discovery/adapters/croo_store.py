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
        
        if token:
            logger.info("CROO bearer token found. Using authenticated API discovery.")
            agents = self._discover_via_api(token)
            if agents:
                return agents
            logger.warning("Authenticated API returned no agents. Falling back to public scraping.")
        
        logger.info(f"Scraping public CROO Agent Store: {CROO_STORE_URL}")
        return self._discover_via_scraping()
    
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
        Parse the public CROO Agent Store HTML for any visible agent metadata.
        Works without authentication.
        """
        agents = []
        
        try:
            response = httpx.get(CROO_STORE_URL, timeout=15.0, follow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Strategy A: Semantic HTML agent cards
            agent_cards = soup.find_all("div", class_=re.compile(
                r"agent|card|listing|grid-item|service", re.I
            ))
            
            for card in agent_cards:
                agent = self._parse_html_card(card)
                if agent:
                    agents.append(agent)
            
            # Strategy B: Next.js RSC / hydration payloads in <script> tags
            if not agents:
                agents = self._parse_nextjs_payloads(soup)
            
            # Strategy C: JSON-LD structured data
            if not agents:
                agents = self._parse_structured_data(soup)
                
        except Exception as e:
            logger.error(f"Public scraping failed: {e}")
        
        logger.info(f"Public scraping discovered {len(agents)} agents.")
        return agents
    
    def _parse_html_card(self, card) -> AgentCreate | None:
        """Extract agent metadata from a semantic HTML card element."""
        name_el = card.find(["h2", "h3", "h4"])
        if not name_el:
            return None
            
        name = name_el.get_text(strip=True)
        if not name or len(name) < 2 or len(name) > 120:
            return None
        
        desc_el = card.find("p")
        description = desc_el.get_text(strip=True) if desc_el else None
        
        price = 0.0
        price_match = re.search(r"\$(\d+\.?\d*)", card.get_text())
        if price_match:
            price = float(price_match.group(1))
            
        capabilities = []
        tag_elements = card.find_all("span", class_=re.compile(r"tag|badge|chip|skill", re.I))
        for tag in tag_elements:
            text = tag.get_text(strip=True).lower().replace(" ", "_")
            if text and len(text) < 50:
                capabilities.append(text)
        
        wallet = None
        wallet_match = re.search(r"(0x[a-fA-F0-9]{40})", card.get_text())
        if wallet_match:
            wallet = wallet_match.group(1)
        
        safe_name = re.sub(r'[^a-z0-9_]', '_', name.lower().strip())
        
        link_el = card.find("a", href=True)
        endpoint = f"croo://store/{safe_name}"
        if link_el:
            href = link_el["href"]
            if href.startswith("/"):
                endpoint = f"croo://store{href}"
        
        return AgentCreate(
            name=name.replace(" ", "_")[:120],
            description=description,
            category="CROO_Marketplace",
            framework="CAP",
            endpoint=endpoint,
            wallet_address=wallet,
            pricing_model="pay_per_call",
            price_per_call=price,
            capabilities=capabilities if capabilities else ["croo_service"],
            staked_tokens=0.0
        )
    
    def _parse_nextjs_payloads(self, soup: BeautifulSoup) -> List[AgentCreate]:
        """Extract agent data from Next.js RSC payloads embedded in <script> tags."""
        agents = []
        script_tags = soup.find_all("script")
        
        for script in script_tags:
            text = script.string
            if not text:
                continue
                
            if not any(kw in text.lower() for kw in ["service", "agent", "skill", "price"]):
                continue
            
            name_matches = re.findall(
                r'"(?:name|title|children)"\s*:\s*"([A-Z][a-zA-Z0-9_ ]{2,60})"', text
            )
            price_matches = re.findall(r'"price"\s*:\s*"?(\d+\.?\d*)"?', text)
            skill_matches = re.findall(r'"(?:skill|tag|category)"\s*:\s*"([^"]+)"', text)
            
            noise_words = {"Next", "React", "Component", "Layout", "Page", "Error",
                          "Loading", "CROO", "Register", "Deploy", "Built", "Store",
                          "Network", "Decentralized", "Agent", "Economy"}
            filtered_names = [n for n in name_matches if n not in noise_words and not n.startswith("$")]
            
            for i, name in enumerate(filtered_names):
                price = float(price_matches[i]) if i < len(price_matches) else 0.0
                caps = [skill_matches[i].lower()] if i < len(skill_matches) else ["croo_service"]
                safe_name = re.sub(r'[^a-z0-9_]', '_', name.lower())
                
                agents.append(AgentCreate(
                    name=name.replace(" ", "_")[:120],
                    category="CROO_Marketplace",
                    framework="CAP",
                    endpoint=f"croo://discovered/{safe_name}",
                    pricing_model="pay_per_call",
                    price_per_call=price,
                    capabilities=caps,
                    staked_tokens=0.0
                ))
        
        return agents
    
    def _parse_structured_data(self, soup: BeautifulSoup) -> List[AgentCreate]:
        """Extract from JSON-LD structured data if present."""
        agents = []
        
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if item.get("@type") in ("Product", "Service", "SoftwareApplication"):
                        name = item.get("name", "")
                        if name:
                            safe_name = re.sub(r'[^a-z0-9_]', '_', name.lower())
                            price = 0.0
                            if "offers" in item:
                                price = float(item["offers"].get("price", 0))
                            agents.append(AgentCreate(
                                name=name.replace(" ", "_")[:120],
                                description=item.get("description"),
                                category="CROO_Marketplace",
                                framework="CAP",
                                endpoint=f"croo://jsonld/{safe_name}",
                                pricing_model="pay_per_call",
                                price_per_call=price,
                                capabilities=["croo_service"],
                                staked_tokens=0.0
                            ))
            except (json.JSONDecodeError, TypeError):
                continue
        
        return agents
