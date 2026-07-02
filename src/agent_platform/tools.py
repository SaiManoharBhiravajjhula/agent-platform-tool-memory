from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ToolFunction = Callable[[str], str]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    run: ToolFunction


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def run(self, name: str, argument: str) -> str:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name].run(argument)

    def names(self) -> list[str]:
        return sorted(self._tools)


def customer_lookup(customer_name: str) -> str:
    data_path = Path(__file__).resolve().parents[2] / "data" / "customers.json"
    customers = json.loads(data_path.read_text(encoding="utf-8"))

    for customer in customers:
        if customer_name.lower() in customer["name"].lower():
            return json.dumps(customer, indent=2)

    return f"No customer found for {customer_name}"


def policy_search(query: str) -> str:
    policies = {
        "renewal": "Renewal risk is high when health score is below 70, usage is declining, or support tickets are unresolved.",
        "support": "Escalate unresolved support tickets before executive renewal conversations.",
        "adoption": "Offer enablement workshops when usage drops by more than 10%.",
    }

    matches = [text for key, text in policies.items() if key in query.lower()]
    return "\n".join(matches or policies.values())


def action_recommender(context: str) -> str:
    recommendations = [
        "Schedule an executive check-in with the account owner.",
        "Create a support escalation plan for unresolved tickets.",
        "Offer an adoption workshop focused on low-usage teams.",
    ]

    if "health_score" in context and "88" in context:
        recommendations = [
            "Confirm renewal timeline.",
            "Identify expansion use cases.",
            "Ask for a customer reference after renewal closes.",
        ]

    return "\n".join(f"- {item}" for item in recommendations)


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(Tool("customer_lookup", "Find customer health and renewal data.", customer_lookup))
    registry.register(Tool("policy_search", "Retrieve internal policy guidance.", policy_search))
    registry.register(Tool("action_recommender", "Recommend next actions from context.", action_recommender))
    return registry