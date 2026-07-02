from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolStep:
    tool_name: str
    argument: str


class RuleBasedPlanner:
    """Deterministic local planner; replace with LangChain/OpenAI in production."""

    def plan(self, user_query: str, available_tools: list[str]) -> list[ToolStep]:
        lower_query = user_query.lower()
        customer = "Acme" if "acme" in lower_query else "Globex" if "globex" in lower_query else "Acme"
        steps: list[ToolStep] = []

        if "customer_lookup" in available_tools:
            steps.append(ToolStep("customer_lookup", customer))
        if "policy_search" in available_tools and any(word in lower_query for word in ["risk", "renewal", "support"]):
            steps.append(ToolStep("policy_search", user_query))
        if "action_recommender" in available_tools:
            steps.append(ToolStep("action_recommender", user_query))

        return steps
