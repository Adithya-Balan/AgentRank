import os
import asyncio
import logging
import json

from croo import AgentClient, Config, EventType, Event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Config(
    base_url=os.getenv("CROO_API_URL", "https://api.croo.network"),
    ws_url=os.getenv("CROO_WS_URL", "wss://api.croo.network/ws")
)
# A generic orchestrator agent's SDK Key paying AgentRank for recommendations
SDK_KEY = os.getenv("CROO_SDK_KEY", "croo_sk_mock_orchestrator")

async def run_requester():
    """
    Simulates a 3rd party Orchestrator Agent querying AgentRank on CAP.
    """
    client = AgentClient(config, SDK_KEY)
    
    try:
        stream = await client.connect_websocket()
        logger.info("✅ Orchestrator connected to CAP.")
    except Exception as e:
        logger.error("Skipping real network connection for demo script (requires valid SK).")
        return
    
    target_service_id = os.getenv("CROO_AGENTRANK_SERVICE_ID", "srv_agentrank123")
    
    # 1. Initiate Negotiation
    logger.info("Initiating negotiation with AgentRank Oracle...")
    req_payload = {
        "service_id": target_service_id,
        "requirements": json.dumps({"capability": "creative_writing"})
    }
    
    try:
        neg = await client.negotiate_order(req_payload)
        logger.info(f"Negotiation created: {neg.id}")
    except Exception as e:
        logger.error(f"Failed to negotiate: {e}")
        await stream.close()
        return

    # 2. Wait for ORDER_CREATED (Provider accepted)
    def on_order_created(e: Event):
        logger.info(f"AgentRank accepted! Order created: {e.order_id}. Paying escrow...")
        async def _pay():
            try:
                await client.pay_order(e.order_id)
                logger.info(f"💸 Paid USDC to CAPVault Escrow for Order {e.order_id}")
            except Exception as err:
                logger.error(f"Payment failed: {err}")
        asyncio.create_task(_pay())
        
    stream.on(EventType.ORDER_CREATED, on_order_created)
    
    # 3. Wait for ORDER_COMPLETED (Provider delivered)
    def on_completed(e: Event):
        logger.info(f"Order completed by AgentRank! Fetching delivery...")
        async def _fetch():
            try:
                delivery = await client.get_delivery(e.order_id)
                logger.info("\n=== 🧠 TRUST INTELLIGENCE RECEIVED ===")
                logger.info(json.dumps(json.loads(delivery.deliverable_text), indent=2))
                logger.info("=======================================\n")
                
                logger.info("Sub-agents successfully discovered! Proceeding to hire sub-agents...")
                await stream.close()
                os._exit(0)
            except Exception as err:
                logger.error(f"Fetch failed: {err}")
        asyncio.create_task(_fetch())
        
    stream.on(EventType.ORDER_COMPLETED, on_completed)
    
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run_requester())
