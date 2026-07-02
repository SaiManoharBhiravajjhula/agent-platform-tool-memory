from __future__ import annotations

from dataclasses import dataclass

from agent_platform.memory import JsonMemoryStore, MemoryRecord
from agent_platform.planner import RuleBasedPlanner
from agent_platform.tools import ToolRegistry, build_default_registry


@dataclass
class AgentResult:
    answer: str
    tools_used: list[str]
    recalled_memory: list[str]


class AgentRunner:
    def __init__(
        self,
        memory: JsonMemoryStore | None = None,
        planner: RuleBasedPlanner | None = None,
        tools: ToolRegistry | None = None,
    ) -> None:
        self.memory = memory or JsonMemoryStore()
        self.planner = planner or RuleBasedPlanner()
        self.tools = tools or build_default_registry()

    def run(self, session_id: str, user_query: str) -> AgentResult:
        recalled = self.memory.search(session_id, user_query)
        steps = self.planner.plan(user_query, self.tools.names())

        observations: list[str] = []
        tools_used: list[str] = []
        current_context = user_query

        for step in steps:
            argument = current_context if step.tool_name == "action_recommender" else step.argument
            observation = self.tools.run(step.tool_name, argument)
            observations.append(f"{step.tool_name}: {observation}")
            tools_used.append(step.tool_name)
            current_context = f"{current_context}\n{observation}"

        answer = self._build_answer(user_query, observations, recalled)

        self.memory.save(
            MemoryRecord(
                session_id=session_id,
                user_message=user_query,
                agent_summary=answer,
                facts=[f"tools_used={','.join(tools_used)}"],
            )
        )

        return AgentResult(
            answer=answer,
            tools_used=tools_used,
            recalled_memory=[item.agent_summary for item in recalled],
        )

    def _build_answer(
        self,
        user_query: str,
        observations: list[str],
        recalled: list[MemoryRecord],
    ) -> str:
        memory_note = f"\nRelevant memory: {recalled[0].agent_summary}" if recalled else ""
        findings = "\n".join(f"- {observation}" for observation in observations)

        return (
            f"Goal: {user_query}\n"
            f"{memory_note}\n"
            "Agent findings:\n"
            f"{findings}\n\n"
            "Recommended response: prioritize customer risk, resolve blockers, and assign clear next actions."
        ).strip()