# Contributing to AgentRank

First off, thank you for considering contributing to AgentRank! We welcome contributions from everyone.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please create an issue in the GitHub repository. Provide as much detail as possible:
* Steps to reproduce the bug
* Expected behavior
* Actual behavior
* Your operating system and Python version

### Suggesting Enhancements
We are always looking for ways to improve AgentRank. Please submit an issue detailing your suggestion, why it's beneficial, and any potential implementation ideas.

### Pull Requests
1. Fork the repository and create your branch from `main`.
2. Ensure you have installed the project via `uv` or `pip`.
3. If you've added code that should be tested, add tests.
4. If you've changed APIs, update the documentation.
5. Ensure your code lints properly.
6. Issue that pull request!

## Project Structure
* `app/`: Core FastAPI application and modules.
* `scripts/`: Testing and CAP Oracle execution scripts.
* `docs/`: Design and architectural documentation.

## Local Development
1. Clone the repo: `https://github.com/Adithya-Balan/AgentRank.git`
2. Install dependencies: `uv sync` or `pip install -r requirements.txt`
3. Run the development server: `uvicorn app.main:app --reload`

Thanks again for helping build the decentralized trust layer for AI!
