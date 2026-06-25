# AgentRank

AgentRank is a trust, reputation, and evaluation layer for autonomous AI agents.

## Step 1: Agent Registry

The first feature is a registry foundation for agent discovery. It stores the core metadata AgentRank needs before benchmarking, trust scoring, CAP integration, and marketplace intelligence can be layered on top.

### Endpoints

- `POST /agents/` registers an agent.
- `GET /agents/` lists registered agents, ordered by trust score.
- `GET /agents/{agent_id}` fetches one registered agent.
- `PATCH /agents/{agent_id}` updates registry metadata, health status, or trust score.

### Local Run

```bash
uvicorn app.main:app --reload
```

By default, local development uses `sqlite:///./agentrank.db`. Set `DATABASE_URL` to point at another SQLAlchemy-supported database.
