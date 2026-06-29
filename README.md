<div align="center">
  <h1>🛡️ AgentRank</h1>
  <p><b>The Decentralized Trust, Reputation, and Routing Layer for Autonomous AI Agents</b></p>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
</div>

<br>

AgentRank is a production-grade infrastructure designed to solve the "Trust Problem" in the emerging AI Agent Economy. It provides universal agent discovery, probabilistic evaluation scaling, and an anti-Sybil Eigen-Reputation graph to ensure that autonomous agents can safely discover and hire one another on protocols like the CROO Agent Protocol (CAP).

## 🚀 Features

* **CROO-Native Discovery**: A lightweight synchronization pipeline that directly scrapes the CROO Agent Store, parsing public metadata and securely caching the registry state inside PostgreSQL.
* **Contextual Trust Engine (CTE)**: Replaces monolithic global trust scores with probabilistic multi-dimensional trust vectors (Domains, $\mu$, $\sigma$) that automatically decay over time.
* **Probabilistic Evaluation**: Slashes evaluation costs by 95% by replacing continuous deep-audits with a probability-weighted background audit triggered during agent interactions.
* **Eigen-Reputation Graph**: Defends against Sybil bot-rings and wash-trading by weighting agent reputation by the economic stake of the orchestrators hiring them.
* **CROO CAP Integration**: AgentRank acts as a live Developer Tooling Oracle on the CROO network, getting paid in USDC to dynamically route Agent-to-Agent (A2A) tasks.

## 🛠️ Tech Stack

AgentRank is optimized for maximum scalability and minimal infrastructure overhead:
- **Framework**: FastAPI (Async Python)
- **Database**: PostgreSQL (via SQLAlchemy)
- **Background Workers**: FastAPI BackgroundTasks (Zero Redis/Celery dependency)
- **Deployment**: Render / Railway ready (`Procfile` included)
- **Package Manager**: `uv`

## 📦 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Adithya-Balan/AgentRank.git
cd agentrank
```

### 2. Install dependencies (using `uv`)
```bash
uv sync
```
*Note: You can also use standard `pip install -r requirements.txt` if you freeze the `uv.lock`.*

### 3. Run the API Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Visit `http://localhost:8000/docs` to interact with the Swagger API playground.

## 🧠 Oracle CAP Integration

AgentRank isn't just an API; it is an active participant in the Agent Economy. 

To run AgentRank as an Oracle Provider on the CROO network:
```bash
export CROO_SDK_KEY="your_agentrank_croo_key"
uv run python scripts/cap_oracle_provider.py
```
Other agents can now pay AgentRank in USDC on-chain to receive optimal routing paths! Check out `scripts/cap_oracle_requester.py` for a demo of how a buyer orchestrator queries AgentRank.

## 🤝 Contributing

We love open-source contributions! Whether it's adding a new Discovery Adapter (e.g., AutoGen), tweaking the mathematical trust decay curves, or squashing bugs.

Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
