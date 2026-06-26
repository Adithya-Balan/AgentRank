import time
import requests

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("--- Step 8: Autonomous Agent Routing ---")

    # 1. Register Source Agent (Orchestrator)
    orch_data = {
        "name": "AutoOrchestrator",
        "category": "Orchestration",
        "endpoint": "https://auto.test",
        "wallet_address": "0xAuto123",
        "price_per_call": 0.0
    }
    
    def get_or_create(data):
        resp = requests.post(f"{BASE_URL}/agents/", json=data)
        if resp.status_code == 409:
            resp = requests.get(f"{BASE_URL}/agents/")
            return next(a["id"] for a in resp.json() if a["name"] == data["name"])
        resp.raise_for_status()
        return resp.json()["id"]

    orch_id = get_or_create(orch_data)

    # 2. Ensure specialized agents exist
    get_or_create({
        "name": "FactCheckerPro",
        "category": "Research",
        "endpoint": "https://fact.test",
        "wallet_address": "0xFact",
        "price_per_call": 0.02,
        "capabilities": ["fact_verification"]
    })
    
    get_or_create({
        "name": "SummaryGenius",
        "category": "Content",
        "endpoint": "https://sum.test",
        "wallet_address": "0xSum",
        "price_per_call": 0.01,
        "capabilities": ["summarization"]
    })

    # 3. Execute Autonomous Routing
    print("Executing Autonomous Routing for a multi-step task...")
    routing_payload = {
        "source_agent_id": orch_id,
        "max_budget": 0.05,
        "tasks": [
            {
                "task_name": "Verify facts in the document",
                "required_capability": "fact_verification"
            },
            {
                "task_name": "Summarize the verified document",
                "required_capability": "summarization"
            }
        ]
    }
    
    resp = requests.post(f"{BASE_URL}/marketplace/route", json=routing_payload)
    resp.raise_for_status()
    result = resp.json()
    
    print("Routing Complete!")
    print(f"Total Cost: ${result['total_cost']}")
    print(f"Budget Remaining: ${result['budget_remaining']}")
    
    for agent in result["hired_agents"]:
        print(f" - Hired {agent['agent_name']} for '{agent['task_name']}' (Tx: {agent['transaction_id']})")
        
    assert len(result["hired_agents"]) == 2
    assert result["total_cost"] == 0.03
    assert result["budget_remaining"] == 0.02
    assert result["status"] == "orchestration_complete"
    
    # 4. Verify Reputation Graph updated
    print("Verifying Reputation Graph for Orchestrator...")
    resp = requests.get(f"{BASE_URL}/reputation/{orch_id}/graph")
    resp.raise_for_status()
    graph = resp.json()
    outbound = graph["outbound_dependencies"]
    
    assert len(outbound) >= 2
    fact_dep = next((d for d in outbound if d["target_agent_name"] == "FactCheckerPro"), None)
    assert fact_dep is not None

    print("\n✅ All Step 8 tests passed!")

if __name__ == "__main__":
    run_tests()
