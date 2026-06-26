import time
import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("--- Step 7: Ranking & Recommendation Layer ---")

    # 1. Create a few agents with different profiles
    agents = [
        {
            "name": "CheapResearchAgent",
            "category": "Research",
            "endpoint": "https://cheap.test",
            "wallet_address": "0xCheap",
            "price_per_call": 0.005,
            "capabilities": ["web_search", "summarization"]
        },
        {
            "name": "PremiumResearchAgent",
            "category": "Research",
            "endpoint": "https://premium.test",
            "wallet_address": "0xPremium",
            "price_per_call": 0.05,
            "capabilities": ["web_search", "citation_validation", "deep_reasoning"]
        },
        {
            "name": "WriterAgent",
            "category": "Content Generation",
            "endpoint": "https://writer.test",
            "wallet_address": "0xWriter",
            "price_per_call": 0.01,
            "capabilities": ["blog_writing", "copywriting"]
        }
    ]
    
    for data in agents:
        resp = requests.post(f"{BASE_URL}/agents/", json=data)
        if resp.status_code != 409:
            resp.raise_for_status()
        
    print("Query: Best research agent under $0.01")
    resp = requests.get(f"{BASE_URL}/rankings/recommend", params={"category": "Research", "max_price": 0.01, "sort_by": "trust_score"})
    resp.raise_for_status()
    results = resp.json()["results"]
    assert len(results) > 0
    assert all(a["price_per_call"] <= 0.01 for a in results)
    assert any(a["name"] == "CheapResearchAgent" for a in results)
    print("✅ Found:", [a["name"] for a in results])

    print("Query: Citation validation agent")
    resp = requests.get(f"{BASE_URL}/rankings/recommend", params={"capability": "citation_validation"})
    resp.raise_for_status()
    results = resp.json()["results"]
    assert len(results) > 0
    assert any(a["name"] == "PremiumResearchAgent" for a in results)
    print("✅ Found:", [a["name"] for a in results])
    
    print("Query: Sort by price")
    resp = requests.get(f"{BASE_URL}/rankings/recommend", params={"sort_by": "price"})
    resp.raise_for_status()
    results = resp.json()["results"]
    assert results[0]["price_per_call"] <= results[1]["price_per_call"]
    print("✅ Ranked by price successfully")

    print("\n✅ All Step 7 tests passed!")

if __name__ == "__main__":
    run_tests()
