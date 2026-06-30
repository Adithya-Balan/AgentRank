import os
import asyncio
import logging
import json

from croo import AgentClient, Config, EventType, Event, DeliverableType
from app.db.database import SessionLocal
from app.rankings.service import get_ranked_agents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CAP Configuration
config = Config(
    base_url=os.getenv("CROO_API_URL", "https://api.croo.network"),
    ws_url=os.getenv("CROO_WS_URL", "wss://api.croo.network/ws")
)
# This would be your AgentRank's registered API Key from the CROO Dashboard
SDK_KEY = os.getenv("CROO_SDK_KEY", "croo_sk_agentrank_oracle_key")

async def run_agentrank_provider():
    """
    Runs AgentRank as an active Provider on the CROO Network (CAP).
    Other agents can pay AgentRank in USDC to fetch trustworthy routing intelligence.
    """
    client = AgentClient(config, SDK_KEY)
    
    try:
        stream = await client.connect_websocket()
        logger.info("✅ Connected to CROO CAP Network. AgentRank Oracle is Online.")
    except Exception as e:
        logger.error(f"Failed to connect to CAP: {e}. (Ensure valid SDK_KEY for real network)")
        # In a real environment, we'd exit here. For the hackathon demo script, we'll continue 
        # so you can see the architecture layout.
        pass

    # 1. Handle incoming queries (Negotiations)
    def on_negotiation(e: Event):
        logger.info(f"Received Agent-to-Agent negotiation request: {e.negotiation_id}")
        async def _accept():
            try:
                # Fetch negotiation terms
                neg = await client.get_negotiation(e.negotiation_id)
                min_price = int(os.getenv("CROO_MIN_PRICE_MICRO_USDC", "10000")) # 0.01 USDC default
                
                # Hardened validation for production: don't accept free or underpriced work
                if neg.fund_amount < min_price:
                    logger.warning(f"Rejecting negotiation {e.negotiation_id}: Insufficient fund amount ({neg.fund_amount} < {min_price})")
                    await client.reject_negotiation(e.negotiation_id, "Insufficient price offered")
                    return
                
                await client.accept_negotiation(e.negotiation_id)
                logger.info(f"Accepted negotiation {e.negotiation_id} for {neg.fund_amount} micro-USDC")
            except Exception as err:
                logger.error(f"Failed to process negotiation: {err}")
        asyncio.create_task(_accept())
        
    try:
        stream.on(EventType.NEGOTIATION_CREATED, on_negotiation)
    except NameError:
        pass

    # 2. Execute Ranking Engine when Paid
    def on_paid(e: Event):
        logger.info(f"💰 Order {e.order_id} paid (USDC locked in CAPVault). Executing query...")
        async def _execute_and_deliver():
            try:
                # Fetch what the requesting agent wants (e.g. "Find best fact-checkers")
                order = await client.get_order(e.order_id)
                req_data = {}
                if hasattr(order, 'requirements') and order.requirements:
                    try:
                        req_data = json.loads(order.requirements)
                    except:
                        req_data = {"capability": str(order.requirements)}
                
                logger.info(f"Querying AgentRank Core for capabilities: {req_data}")
                
                # Hit local DB to get rankings
                db = SessionLocal()
                try:
                    agents = get_ranked_agents(
                        db,
                        capability=req_data.get("capability", "fact_checking"),
                        category=req_data.get("category"),
                        limit=3
                    )
                    
                    results = []
                    for a in agents.results:
                        results.append({
                            "agent_id": a.agent_id,
                            "name": a.name,
                            "trust_score": a.overall_trust_score,
                            "price_per_call": a.price_per_call
                        })
                        
                    deliverable_payload = json.dumps({"recommended_agents": results})
                finally:
                    db.close()
                
                # Deliver the data back to the protocol to release the USDC to our wallet
                await client.deliver_order(
                    e.order_id, 
                    {"deliverable_type": DeliverableType.SCHEMA, "deliverable_text": deliverable_payload}
                )
                logger.info(f"🚀 Delivered trust intelligence for Order {e.order_id}. Settlement complete.")
                
            except Exception as err:
                logger.error(f"Delivery failed: {err}")
                
        asyncio.create_task(_execute_and_deliver())
        
    try:
        stream.on(EventType.ORDER_PAID, on_paid)
    except NameError:
        pass
    
    logger.info("Listening for A2A commerce events...")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down AgentRank Oracle...")
        if 'stream' in locals():
            await stream.close()

if __name__ == "__main__":
    asyncio.run(run_agentrank_provider())
