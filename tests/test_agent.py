from agent_platform.agent import AgentRunner
from agent_platform.memory import JsonMemoryStore


def test_agent_runs_tools_and_saves_memory(tmp_path):
    memory = JsonMemoryStore(tmp_path / "memory.json")
    runner = AgentRunner(memory=memory)

    result = runner.run("session-1", "Check renewal risk for Acme and draft next actions")

    assert "customer_lookup" in result.tools_used
    assert "action_recommender" in result.tools_used
    assert "Acme" in result.answer
    assert memory.load_session("session-1")
