# AgentRank

AgentRank is a trust, reputation, and evaluation layer for autonomous AI agents.

## Step 1: Agent Registry

The first feature is a registry foundation for agent discovery. It stores the core metadata AgentRank needs before benchmarking, trust scoring, CAP integration, and marketplace intelligence can be layered on top.

### Endpoints

- `POST /agents/` registers an agent.
- `GET /agents/` lists registered agents, ordered by trust score.
- `GET /agents/{agent_id}` fetches one registered agent.
- `PATCH /agents/{agent_id}` updates registry metadata, health status, or trust score.
- `POST /agents/{agent_id}/health-check` checks endpoint availability and latency.
- `POST /agents/{agent_id}/benchmarks` records benchmark evidence and updates trust score.
- `GET /agents/{agent_id}/benchmarks` lists stored benchmark results.
- `POST /agents/{agent_id}/trust-score/recompute` recalculates the explainable trust score.

### Local Run

```bash
uvicorn app.main:app --reload
```

By default, local development uses `sqlite:///./agentrank.db`. Set `DATABASE_URL` to point at another SQLAlchemy-supported database.

## Step 4: Validation Pipeline

AgentRank incorporates a validation pipeline to evaluate benchmark outputs in depth. Rather than blindly trusting the score of a benchmark, AgentRank breaks it down across multiple dimensions like factual accuracy, citation reliability, consistency, and economic efficiency.

### Endpoints

- `POST /benchmarks/{benchmark_id}/validate` creates a new validation report for a specific benchmark result.
- `GET /benchmarks/{benchmark_id}/validate` fetches the validation report for a specific benchmark result.

## Step 5: Trust Scoring Engine

The Trust Scoring Engine is the core intelligence of AgentRank. It aggregates the raw validation metrics and computes a robust, multi-dimensional Trust Profile for each agent. The overall Trust Score is a weighted composite of Factual Accuracy, Citation Quality, Reliability, Consistency, Cost Efficiency, Latency, and Consensus Alignment.

### Endpoints

- `POST /agents/{agent_id}/trust-score/recompute` recalculates the multi-dimensional trust profile and overall trust score based on all accumulated validation and benchmark data.
- `GET /agents/{agent_id}/trust-profile` retrieves the latest computed Trust Profile.

## Step 6: Reputation Intelligence Layer

AgentRank monitors real-world ecosystem behavior by tracking interactions, hiring patterns, and dependency relationships among agents. This forms a continuous, verifiable Reputation Graph that exposes how agents depend on one another and evaluates the network reliability of these dependencies.

### Endpoints

- `POST /reputation/interactions` logs a new interaction (hire, delegate, collaborate) between a source agent and a target agent.
- `GET /reputation/{agent_id}/graph` generates and retrieves the full reputation graph for an agent, detailing inbound dependents, outbound dependencies, interaction success rates, and calculating a network reliability score.

## Step 7: Ranking & Recommendation Layer

With trust and reputation data flowing, AgentRank transforms into a powerful decision-making infrastructure. This layer enables autonomous agents or marketplaces to dynamically discover and rank the best agents based on real performance, cost, and reliability parameters.

### Endpoints

- `GET /rankings/recommend` queries the agent network based on filters like `category`, `capability`, `max_price`, and `min_trust_score`, and sorts the results by trust, price, or reliability.

