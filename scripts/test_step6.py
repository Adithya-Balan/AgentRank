import time
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("--- Step 6: Reputation Intelligence Layer ---")

    # 1. Create two agents
    agent_data_1 = {
        "name": "OrchestratorAgent",
        "category": "Orchestration",
        "endpoint": "https://orch.test.example.com",
        "wallet_address": "0xOrch123",
        "price_per_call": 0.0
    }
    agent_data_2 = {
        "name": "WorkerAgent",
        "category": "Research",
        "endpoint": "https://worker.test.example.com",
        "wallet_address": "0xWorker123",
        "price_per_call": 0.05
    }
    
    def get_or_create(data):
        resp = requests.post(f"{BASE_URL}/agents/", json=data)
        if resp.status_code == 409:
            resp = requests.get(f"{BASE_URL}/agents/")
            return next(a["id"] for a in resp.json() if a["name"] == data["name"])
        resp.raise_for_status()
        return resp.json()["id"]

    orch_id = get_or_create(agent_data_1)
    worker_id = get_or_create(agent_data_2)

    # 2. Log interactions
    interaction_data = {
        "source_agent_id": orch_id,
        "target_agent_id": worker_id,
        "interaction_type": "hire",
        "success": True,
        "task_description": "Summarize research paper",
        "cost_incurred": 0.05,
        "latency_ms": 1500.0
    }
    print("Logging interaction 1 (Orchestrator -> Worker)...")
    resp = requests.post(f"{BASE_URL}/reputation/interactions", json=interaction_data)
    resp.raise_for_status()
    print("Interaction logged:", resp.json()["id"])

    interaction_data["latency_ms"] = 1200.0
    print("Logging interaction 2 (Orchestrator -> Worker)...")
    resp = requests.post(f"{BASE_URL}/reputation/interactions", json=interaction_data)
    resp.raise_for_status()
    print("Interaction logged:", resp.json()["id"])
    
    # 3. Fetch Reputation Graph for Orchestrator
    print(f"Fetching Reputation Graph for Orchestrator (ID: {orch_id})...")
    resp = requests.get(f"{BASE_URL}/reputation/{orch_id}/graph")
    resp.raise_for_status()
    graph = resp.json()
    print("Reputation Graph for Orchestrator:")
    print(graph)
    
    # Simple verifications
    assert graph["agent_name"] == "OrchestratorAgent"
    assert len(graph["outbound_dependencies"]) > 0
    
    # Find WorkerAgent in outbound dependencies
    worker_dep = next((d for d in graph["outbound_dependencies"] if d["target_agent_id"] == worker_id), None)
    assert worker_dep is not None
    assert worker_dep["success_rate"] == 100.0
    assert worker_dep["average_latency_ms"] == 1350.0  # (1500 + 1200) / 2
    
    # 4. Fetch Reputation Graph for Worker
    print(f"Fetching Reputation Graph for Worker (ID: {worker_id})...")
    resp = requests.get(f"{BASE_URL}/reputation/{worker_id}/graph")
    resp.raise_for_status()
    graph_worker = resp.json()
    
    orch_dep = next((d for d in graph_worker["inbound_dependents"] if d["target_agent_id"] == orch_id), None)
    assert orch_dep is not None
    assert orch_dep["interaction_count"] >= 2

    print("\n✅ All Step 6 tests passed!")

if __name__ == "__main__":
    run_tests()
