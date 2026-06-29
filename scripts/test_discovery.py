import time
import requests

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("--- Scalable Agent Discovery Testing ---")

    print("Triggering the Discovery Crawler...")
    resp = requests.post(f"{BASE_URL}/discovery/run")
    resp.raise_for_status()
    result = resp.json()
    
    print(f"Crawled Sources: {result['sources_crawled']}")
    print(f"Total Found: {result['total_found']}")
    print(f"New Agents Added: {result['new_added']}")
    
    # Run again to ensure idempotency (no duplicates added)
    print("\nRe-running crawler to test deduplication...")
    resp2 = requests.post(f"{BASE_URL}/discovery/run")
    resp2.raise_for_status()
    result2 = resp2.json()
    
    print(f"New Agents Added on second run: {result2['new_added']}")
    assert result2['new_added'] == 0, "Duplicate agents were added!"
    
    # Query rankings to see if we can find the discovered agents
    print("\nQuerying Rankings to find discovered MCP agent...")
    resp_rank = requests.get(f"{BASE_URL}/rankings/recommend", params={"capability": "sql_query"})
    resp_rank.raise_for_status()
    found = resp_rank.json()["results"]
    assert len(found) > 0
    assert found[0]["name"] == "MCP_PostgresConnector"
    print(f"✅ Discovered agent is live in AgentRank: {found[0]['name']}")

    print("\n✅ All Discovery tests passed!")

if __name__ == "__main__":
    run_tests()
