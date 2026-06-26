import time
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("--- Step 5: Trust Scoring Engine ---")

    print("Registering agent...")
    agent_data = {
        "name": "TrustEngineTestAgent",
        "category": "Reasoning",
        "endpoint": "https://trust.test.example.com",
        "wallet_address": "0xTrust123",
        "description": "Agent for trust scoring engine test",
        "price_per_call": 0.05
    }
    resp = requests.post(f"{BASE_URL}/agents/", json=agent_data)
    if resp.status_code == 409:
        resp = requests.get(f"{BASE_URL}/agents/")
        agent_id = next(a["id"] for a in resp.json() if a["name"] == "TrustEngineTestAgent")
    else:
        resp.raise_for_status()
        agent_id = resp.json()["id"]

    print("Creating benchmark result...")
    benchmark_data = {
        "benchmark_name": "Multi-dimensional Evaluation Task",
        "task_type": "reasoning",
        "score": 90,
        "passed": True,
        "latency_ms": 400, # Sub-500ms -> latency score 100
        "cost_usd": 0.05,
        "evaluator": "automated",
    }
    resp = requests.post(f"{BASE_URL}/agents/{agent_id}/benchmarks", json=benchmark_data)
    resp.raise_for_status()
    benchmark_id = resp.json()["id"]

    print(f"Creating validation report for benchmark {benchmark_id}...")
    validation_data = {
        "factual_accuracy_score": 90.0,
        "hallucination_rate": 5.0, # Will penalize accuracy by 5.0
        "citation_reliability_score": 80.0,
        "prompt_adherence_score": 100.0,
        "consistency_score": 95.0,
        "reasoning_quality_score": 90.0,
        "economic_efficiency_score": 85.0,
        "details": {}
    }
    resp = requests.post(f"{BASE_URL}/benchmarks/{benchmark_id}/validate", json=validation_data)
    if resp.status_code != 409:
        resp.raise_for_status()

    print("Recomputing Trust Profile...")
    resp = requests.post(f"{BASE_URL}/agents/{agent_id}/trust-score/recompute")
    resp.raise_for_status()
    profile = resp.json()
    
    print("Trust Profile Recomputed:", profile)
    assert profile["accuracy_score"] == 85.0  # 90 - 5
    assert profile["citation_quality_score"] == 80.0
    assert profile["latency_score"] == 100.0
    print("Overall Trust Score:", profile["overall_trust_score"])
    
    print("Fetching Trust Profile via GET...")
    resp = requests.get(f"{BASE_URL}/agents/{agent_id}/trust-profile")
    resp.raise_for_status()
    assert resp.json()["overall_trust_score"] == profile["overall_trust_score"]

    print("\n✅ All Step 5 tests passed!")

if __name__ == "__main__":
    run_tests()
