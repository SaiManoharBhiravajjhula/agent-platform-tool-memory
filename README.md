# Agent Platform with Tool Use and Memory

This project demonstrates an AI agent platform that can reason through a user request, choose tools, call APIs or local data sources, and remember useful context across sessions.

The code is intentionally small and readable for interviews. It runs locally without paid services, and the README shows where Redis, LangChain, and OpenAI plug in for a production version.

## What This Project Shows

- Multi-step agent execution with a planner, tools, and final response generation
- Tool use across mock APIs, document search, and a small customer database
- Session memory with a local JSON store and a Redis-ready interface
- Vector-style memory search for recalling relevant previous interactions
- Clear logging of each step so the workflow is easy to explain

## Architecture

```text
User request -> AgentRunner -> MemoryStore -> Planner -> ToolRegistry -> Final response
```

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH="src"
python -m agent_platform.main --session demo-user --query "Check renewal risk for Acme and draft next actions"
pytest
```

## Production Integration Notes

- Replace `RuleBasedPlanner` with a LangChain/OpenAI tool-calling agent.
- Replace `JsonMemoryStore` with a Redis implementation.
- Replace sample customer JSON with CRM or database queries.
- Replace local document search with Pinecone, Redis Vector, or Azure AI Search.

## Project Structure

```text
src/agent_platform/
  agent.py      - Orchestrates planning, tools, memory, and response
  memory.py     - Session memory and simple semantic recall
  planner.py    - Converts a request into tool steps
  tools.py      - Tool registry and business task tools
  main.py       - Command line entry point
tests/          - Unit tests
data/           - Sample business dataset
```
