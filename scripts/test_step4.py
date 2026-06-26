import time
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("--- Step 4: Validation Pipeline ---")

    print("Registering agent...")
    agent_data = {
        "name": "ValidationTestAgent",
        "category": "Reasoning",
        "endpoint": "https://val.test.example.com",
        "wallet_address": "0xVal123",
        "description": "Agent for validation pipeline test",
        "price_per_call": 0.05
    }
    resp = requests.post(f"{BASE_URL}/agents/", json=agent_data)
    if resp.status_code == 409:
        print("Agent already exists. Fetching from DB.")
        resp = requests.get(f"{BASE_URL}/agents/")
        agent_id = next(a["id"] for a in resp.json() if a["name"] == "ValidationTestAgent")
    else:
        resp.raise_for_status()
        agent_id = resp.json()["id"]

    print("Creating benchmark result...")
    benchmark_data = {
        "benchmark_name": "Complex Reasoning Task",
        "task_type": "reasoning",
        "score": 90,
        "passed": True,
        "latency_ms": 1200,
        "cost_usd": 0.05,
        "evaluator": "automated",
        "prompt": "Solve the traveling salesperson problem for 5 cities...",
        "actual_output": "The shortest path is A->C->E->B->D->A with total distance 145."
    }
    resp = requests.post(f"{BASE_URL}/agents/{agent_id}/benchmarks", json=benchmark_data)
    resp.raise_for_status()
    benchmark_id = resp.json()["id"]

    print(f"Creating validation report for benchmark {benchmark_id}...")
    validation_data = {
        "factual_accuracy_score": 95.0,
        "hallucination_rate": 2.0,
        "citation_reliability_score": 100.0,
        "prompt_adherence_score": 98.0,
        "consistency_score": 99.0,
        "reasoning_quality_score": 96.0,
        "economic_efficiency_score": 85.0,
        "details": {
            "notes": "Excellent reasoning. Minor hallucination regarding non-existent algorithm names."
        }
    }
    resp = requests.post(f"{BASE_URL}/benchmarks/{benchmark_id}/validate", json=validation_data)
    if resp.status_code == 409:
        print("Validation report already exists. Continuing test.")
    else:
        resp.raise_for_status()
        report = resp.json()
        print("Validation Report Created:", report)

    print("Fetching validation report...")
    resp = requests.get(f"{BASE_URL}/benchmarks/{benchmark_id}/validate")
    resp.raise_for_status()
    report_fetched = resp.json()
    print("Fetched Score:", report_fetched["overall_validation_score"])
    
    print("\n✅ All Step 4 tests passed!")

if __name__ == "__main__":
    run_tests()
