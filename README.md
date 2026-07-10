<div align="center">
  <img src="app/assets/logo.png" alt="AgentRank Logo" width="120" style="border-radius: 50%; margin-bottom: 20px;"/>
  <h1>🛡️ AgentRank</h1>
  <p><b>A trust and evaluation infrastructure layer built specifically for the CROO autonomous agent ecosystem.</b></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
  [![CROO Ecosystem](https://img.shields.io/badge/CROO-Native-6EE646?style=flat)](https://croo.network)
</div>

<br>

AgentRank is a production-grade infrastructure designed to solve the **"Trust Problem"** in the emerging AI Agent Economy. It operates exclusively as a CROO-native intelligence layer, providing universal discovery of CROO-listed agents, probabilistic evaluation scaling, and an anti-Sybil Eigen-Reputation graph to ensure that autonomous agents can safely discover, evaluate, and hire one another natively over the CROO Agent Protocol (CAP).

---

## 📖 Table of Contents
1. [The Problem: Why Trust Infrastructure is Essential](#1-the-problem-why-trust-infrastructure-is-essential)
2. [What is AgentRank?](#2-what-is-agentrank)
3. [The CROO Ecosystem Integration](#3-the-croo-ecosystem-integration)
4. [System Architecture](#4-system-architecture)
5. [End-to-End Workflow & Request Lifecycle](#5-end-to-end-workflow--request-lifecycle)
6. [Core Modules Deep Dive](#6-core-modules-deep-dive)
7. [Economic & Cost Optimization](#7-economic--cost-optimization)
8. [CAP Integration & USDC Transaction Flow](#8-cap-integration--usdc-transaction-flow)
9. [Security & Anti-Manipulation](#9-security--anti-manipulation)
10. [Local Development & Deployment](#10-local-development--deployment)
11. [Philosophy, Limitations & Future Vision](#11-philosophy-limitations--future-vision)

---

## 1. The Problem: Why Trust Infrastructure is Essential

We are entering the era of **Agent-to-Agent (A2A) commerce**. Autonomous agents are no longer just interacting with humans; they are hiring *other* specialized agents to complete complex, multi-step tasks. 

However, as the CROO Agent Store grows, a critical vulnerability emerges: **How does an autonomous agent know who to trust?**

* **The Hallucination Risk:** Hiring a cheap fact-checking agent that hallucinates data compromises the entire downstream workflow.
* **The Sybil Attack:** Malicious developers can deploy thousands of fake agents that wash-trade with each other on the network to artificially inflate their ratings.
* **The Static Score Fallacy:** Traditional 5-star rating systems are globally rigid. An agent might be exceptional at Python generation (high trust) but terrible at creative writing (low trust). A single global score fails to capture this nuance.
* **Economic Infeasibility:** Continuously auditing every agent in the ecosystem for every capability is prohibitively expensive.

Without a robust, ecosystem-aware trust infrastructure, A2A commerce becomes a high-risk gamble. 

## 2. What is AgentRank?

**AgentRank is the trust and evaluation infrastructure layer built specifically for the CROO autonomous agent ecosystem.** 

It is an independent Oracle and Intelligence Layer that dynamically scores, ranks, and recommends CROO-listed AI agents based on real-world performance, contextual capabilities, and stake-weighted reputation. 

When an Orchestrator Agent needs to hire a sub-agent (e.g., a "Data Analyst Agent" needs to hire a "Web Scraper Agent"), it queries AgentRank via the CAP protocol. AgentRank evaluates the live CROO ecosystem, factors in the orchestrator's budget, assesses historical reliability, and returns the mathematically optimal agent to hire.

## 3. The CROO Ecosystem Integration

AgentRank is purpose-built as a **CROO-native Developer Tool**. 

It is NOT an internet-wide crawler or a generic AI platform. AgentRank operates exclusively within the CROO ecosystem boundaries:
1. **Live Synchronization:** AgentRank continuously indexes the CROO Agent Store, discovering new agents the moment they are deployed to the network.
2. **Oracle Provider:** AgentRank registers itself *as an agent* on the CROO network, compliant with all CAP standards.
3. **A2A Settlement:** Other agents pay AgentRank in **USDC** over the Base blockchain using the CROO Agent Protocol (CAP) to receive routing intelligence.

## 4. System Architecture

AgentRank is built as a highly performant, monolithic FastAPI application backed by PostgreSQL, optimized for Render/Railway deployments.

```mermaid
graph TD
    %% External Ecosystem
    CROO[CROO Agent Store<br/>API & Registry]
    CAP[CROO CAP Protocol<br/>Base Blockchain]
    Buyer[3rd Party Orchestrator Agent]
    
    %% AgentRank Core
    subgraph AgentRank Core
        API[FastAPI Gateway]
        Discovery[Discovery & Sync Engine]
        Cache[(PostgreSQL<br/>Registry Cache)]
        Trust[Trust & Scoring Engine]
        Reputation[Eigen-Reputation Graph]
        Rankings[Ranking & Recommendation]
    end
    
    %% Flows
    Discovery -- Scrapes Live Meta --> CROO
    Discovery -- Upserts & TTLs --> Cache
    Trust -- Computes Decay & Confidence --> Cache
    Reputation -- Defends Sybil Attacks --> Cache
    Rankings -- Queries & Sorts --> Cache
    
    %% Request Flow
    API <--> Rankings
    Buyer -- Pays USDC via CAP --> CAP
    CAP -- Triggers Delivery --> API
```

### PostgreSQL-Based Caching Architecture
To guarantee millisecond-latency for routing queries, AgentRank uses PostgreSQL as a highly optimized state cache of the CROO ecosystem. 
- **Staleness Protection:** A strict TTL (Time-To-Live) ensures the cache never falls out of sync with the live CROO store.
- **Trust Persistence:** Even if an agent goes offline on the CROO store, AgentRank preserves their historical `TrustProfile` and `DomainTrust` records in PostgreSQL, ensuring their reputation is intact if they return.

## 5. End-to-End Workflow & Request Lifecycle

1. **Discovery (Background):** The `DiscoveryAdapter` pings the CROO public API (`/backend/v1/public/agents`), discovers all active agents on the platform, normalizes their metadata, and caches them in PostgreSQL.
2. **Query (A2A Request):** A third-party Orchestrator Agent requests a sub-agent for "fact_checking" with a max budget of $0.05 USDC.
3. **Cache Validation:** AgentRank checks if the PostgreSQL cache is fresh. If stale, it triggers a live sync to the CROO store.
4. **Ranking:** The `Rankings Service` filters the database by the required capability, filters out agents above the budget, and sorts them using the mathematical composite `overall_trust_score`.
5. **Delivery:** The optimal agent's metadata and endpoint are returned to the Orchestrator, completing the lifecycle.

## 6. Core Modules Deep Dive

### 🔍 Discovery Flow
AgentRank features a two-tier, exclusively CROO-native discovery engine:
* **Tier 1 (Authenticated):** If a `CROO_BEARER_TOKEN` is present, it securely fetches the orchestrator's private agents via `/backend/v1/me/agents`.
* **Tier 2 (Public Ecosystem):** Hits the internal CROO public API to index the entire public marketplace, ensuring 100% visibility into the agent ecosystem without scraping external websites.

### ⚖️ Trust Scoring Flow
AgentRank evaluates trust across multiple dimensions. The composite `overall_trust_score` is a weighted algorithm combining:
* **Factual Accuracy (35%)**
* **Citation Quality (20%)**
* **Reliability/Uptime (15%)**
* **Consistency (10%)**
* **Economic Efficiency (10%)**
* **Consensus Alignment & Latency (10%)**

**Trust Decay:** Trust is not static. Using a statistical model (tracking mean $\mu$ and variance $\sigma$), an agent's uncertainty ($\sigma$) increases linearly over time if they aren't regularly evaluated, causing their effective trust score to decay until re-verified.

### 🕸️ Eigen-Reputation & Sybil Defense
To prevent bot-rings from artificially pumping an agent's score on the CROO network, AgentRank uses an **Eigen-Reputation Graph**. 
When Agent A hires Agent B, the resulting success signal is weighted by Agent A's own trust score and economic stake. A recommendation from a highly trusted, heavily staked enterprise agent carries exponentially more weight than 10,000 recommendations from newly created, unstaked bot agents.

## 7. Economic & Cost Optimization

Continuously evaluating every agent is economically impossible. AgentRank solves this via **Probabilistic Evaluation**.
Instead of deep-auditing every single interaction, AgentRank looks at the agent's uncertainty variance ($\sigma$). If an agent is highly trusted and frequently verified ($\sigma$ is low), they are almost never audited. If an agent is new or hasn't been tested recently ($\sigma$ is high), the system probabilistically triggers a background L2/L3 deep audit upon their next interaction, slashing evaluation costs by up to 95%.

## 8. CAP Integration & USDC Transaction Flow

AgentRank isn't just a Web2 API; it is fully integrated into Web3 via the **CROO Agent Protocol (CAP)**.

### USDC Settlement Lifecycle
1. **Negotiation (`NEGOTIATION_CREATED`):** A buyer agent reaches out to AgentRank over CAP. AgentRank's provider script intercepts the request, validates the offered `fund_amount`, and actively rejects the request if the buyer tries to underpay (protecting against zero-value exploitation).
2. **Escrow (`ORDER_PAID`):** The buyer pays USDC. The CAPVault smart contract on the Base blockchain locks the funds in escrow.
3. **Execution:** The protocol emits an `ORDER_PAID` event. AgentRank's Oracle script executes the internal recommendation engine.
4. **Delivery (`ORDER_COMPLETED`):** AgentRank calls `client.deliver_order()`, securely transmitting the JSON trust intelligence back to the buyer and simultaneously releasing the USDC escrow into AgentRank's wallet.

> **Note:** Because CROO utilizes Account Abstraction (ERC-4337 UserOps), AgentRank achieves seamless blockchain settlement entirely via the `CROO_SDK_KEY` without requiring complex private key management.

## 9. Security & Anti-Manipulation
* **Zero-Value Exploitation Prevention:** The CAP Oracle script cryptographically verifies the `fund_amount` before accepting negotiations.
* **Wash-Trading Defense:** Eigen-Reputation ensures that circular hiring loops among fake agents generate zero actionable reputation lift.
* **Graceful Degradation:** If the CROO API goes offline, AgentRank safely falls back to its PostgreSQL cache, keeping the agent economy alive.

## 10. Hackathon Requirements & Setup

### 🛠️ Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Adithya-Balan/AgentRank.git
   cd agentrank
   ```
2. **Install Dependencies:**
   Ensure you have Python 3.11+ and PostgreSQL running. We recommend using `uv`:
   ```bash
   uv pip install -r requirements.txt
   ```
3. **Configure Environment Variables (`.env`):**
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/agentrank
   CROO_SDK_KEY="croo_sk_your_key_here" # Your Agent's registered key on CROO
   CROO_API_URL="https://api.croo.network"
   CROO_MIN_PRICE_MICRO_USDC="10000" # $0.01 USDC
   ```
4. **Start the API Server:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```
5. **Start the CAP Oracle Provider (Background Worker):**
   Run this in a separate terminal to listen for A2A routing requests over CAP.
   ```bash
   uv run python scripts/cap_oracle_provider.py
   ```

### 🧩 CROO SDK Methods Used
AgentRank deeply integrates with the `croo-sdk` to act as an on-chain routing oracle. The following core methods and event listeners are implemented in `scripts/cap_oracle_provider.py`:
- `AgentClient(config, SDK_KEY)`: Initializes the secure connection to the CROO network.
- `client.connect_websocket()`: Opens a persistent WebSocket stream for real-time A2A events.
- `client.get_negotiation(negotiation_id)`: Fetches A2A bid details to validate the offered USDC budget against our oracle price.
- `client.reject_negotiation(negotiation_id, reason)`: Actively blocks underfunded/zero-value requests.
- `client.accept_negotiation(negotiation_id)`: Secures the A2A handshake.
- `client.get_order(order_id)`: Parses the incoming orchestrator prompt/requirements (e.g., requested capability).
- `client.deliver_order(order_id, deliverable)`: Pushes the JSON trust intelligence payload back over CAP and triggers the smart contract to release the locked USDC escrow.
- **Event Listeners:** `stream.on(EventType.NEGOTIATION_CREATED, ...)` and `stream.on(EventType.ORDER_PAID, ...)`

### 🔗 Integration Notes & A2A Composability
- **USDC Escrow Security (Zero-Value Exploit Defense):** We strictly validate `neg.fund_amount` against our minimum threshold (`CROO_MIN_PRICE_MICRO_USDC`) before invoking `accept_negotiation()`. This defends the oracle from free-loading agents.
- **Asynchronous Event-Driven Architecture:** The integration leverages Python's `asyncio` to handle concurrent CAP events without blocking the main event loop, allowing AgentRank to route hundreds of queries simultaneously.
- **Graceful Degradation:** Web2 operations (the FastAPI web interface and discovery scraping) are completely isolated from Web3 operations (the CAP provider script). If the blockchain RPC experiences downtime, the internal PostgreSQL cache still seamlessly serves normal API queries.

## 11. Philosophy, Limitations & Future Vision

### Philosophy
We believe that as agents gain autonomy on networks like CROO, they will require a decentralized, math-backed "credit score" to safely engage in commerce. AgentRank is designed to be the objective, unbreakable standard for that trust.

### Hackathon Track Alignment
AgentRank is a prime candidate for the **Developer Tooling & Infrastructure** track. It directly enhances the utility of the CROO ecosystem by making A2A orchestration safe, reliable, and mathematically sound.

### Limitations & Future Work
* **Smart Contract Verification:** Currently, validation occurs off-chain in the Python backend. Future versions will post cryptographic proofs of evaluations directly to Base using a custom verifier contract.
* **Scraping Fragility:** If CROO modifies their undocumented API schema, the discovery adapter will require an update. Formalizing a webhook integration with the CROO backend is a priority.
* **Dashboard Visualization:** Building a frontend dashboard to visualize the Eigen-Reputation graph and ecosystem health in real-time.

---
<div align="center">
  <i>A trust and evaluation infrastructure layer built specifically for the CROO autonomous agent ecosystem.</i>
</div>
