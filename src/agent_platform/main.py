from __future__ import annotations

import argparse
import os

from agent_platform.agent import AgentRunner
from agent_platform.memory import JsonMemoryStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the agent platform demo.")
    parser.add_argument("--session", default="demo-user", help="Stable user or account session id.")
    parser.add_argument("--query", required=True, help="Business request for the agent.")
    args = parser.parse_args()

    runner = AgentRunner(memory=JsonMemoryStore(os.getenv("MEMORY_FILE", ".agent_memory.json")))
    result = runner.run(args.session, args.query)

    print(result.answer)
    print(f"\nTools used: {', '.join(result.tools_used)}")


if __name__ == "__main__":
    main()