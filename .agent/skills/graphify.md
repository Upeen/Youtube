## graphify

This project has a high-fidelity Graphify knowledge graph providing structural insights into the YouTube Analytics Engine.

Rules:
- Before resolving architectural tickets or complex refactoring, read the Graphify summary in `AGENTS.md` and the `PROJECT_DOCUMENTATION.md`.
- Prioritize understanding "God Nodes" (central agents like `recommender.py`) before modifying peripheral logic.
- If the Graphify MCP server is available, use `query_graph` to trace data flow from the Harvester (`fetch_data.py`) to the Orchestrator (`app.py`).
- Maintain the graph: After any major structural logic changes (e.g., adding a new agent style), run `graphify update .` to sync the AST-based relationship map.
