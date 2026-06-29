"""
CROO OAuth Authentication Helper for AgentRank.

Since the CROO Agent Store requires authentication to access agent listings,
this script obtains a bearer token via CROO's Google OAuth flow.

Usage:
    PYTHONPATH=. uv run python scripts/croo_auth.py

After completing the OAuth flow, paste the token into your .env file:
    CROO_BEARER_TOKEN=eyJhbG...
"""
import os
import sys
import json
import httpx

CROO_API = "https://api.croo.network/backend/v1"

def main():
    print("=" * 60)
    print("  CROO OAuth Authentication for AgentRank")
    print("=" * 60)
    print()
    
    # Step 1: Get Google OAuth URL from CROO
    print("[1/3] Requesting Google OAuth URL from CROO...")
    resp = httpx.get(
        f"{CROO_API}/auth/url",
        params={
            "flow": "login",
            "type": "google",
            "redirect_url": "https://agent.croo.network/auth/callback?method=google&mode=agent"
        },
        timeout=10.0
    )
    resp.raise_for_status()
    auth_url = resp.json().get("authUrl")
    
    if not auth_url:
        print("ERROR: Could not get OAuth URL from CROO.")
        sys.exit(1)
    
    print()
    print("[2/3] Open this URL in your browser and sign in with Google:")
    print()
    print(f"  {auth_url}")
    print()
    print("After signing in, you will be redirected to a callback page.")
    print("Copy the JSON credential shown on that page.")
    print()
    
    # Step 2: User pastes the credential
    credential_str = input("Paste the credential JSON here: ").strip()
    
    try:
        credential = json.loads(credential_str)
        token = credential.get("token", credential_str)
    except json.JSONDecodeError:
        # Maybe they just pasted the raw token
        token = credential_str
    
    if not token:
        print("ERROR: No token found in credential.")
        sys.exit(1)
    
    # Step 3: Verify the token works
    print()
    print("[3/3] Verifying token with CROO API...")
    
    verify_resp = httpx.get(
        f"{CROO_API}/me/agents",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0
    )
    
    if verify_resp.status_code == 200:
        data = verify_resp.json()
        agents = data if isinstance(data, list) else data.get("agents", data.get("data", []))
        print(f"✅ Token valid! Found {len(agents)} agents in your CROO account.")
        
        for a in agents:
            if isinstance(a, dict):
                print(f"   - {a.get('name', 'unnamed')} (ID: {a.get('id', 'unknown')})")
    elif verify_resp.status_code == 401:
        print("❌ Token is invalid or expired. Try authenticating again.")
        sys.exit(1)
    else:
        print(f"⚠️  Unexpected response: {verify_resp.status_code} - {verify_resp.text[:200]}")
    
    # Save to .env
    print()
    print("Add this to your .env file:")
    print()
    print(f'CROO_BEARER_TOKEN="{token}"')
    print()
    print("Then restart your uvicorn server and run: POST /discovery/sync")

if __name__ == "__main__":
    main()
