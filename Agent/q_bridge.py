"""Bridge between Q-lang semantic operations and the existing agent engine."""
from typing import Any

try:
    from Agent.agent import QLangAgentEngine
except ImportError:
    QLangAgentEngine = None


class QAgentBridge:
    """Delegate protocol instructions to the Q-lang agent layer."""

    def __init__(self, agent=None, agent_name: str = "q-lang"):
        if agent is not None:
            self.agent = agent
        elif QLangAgentEngine is not None:
            self.agent = QLangAgentEngine(agent_name=agent_name)
        else:
            self.agent = None

    def coordinate(self, action: str, context: Any = None):
        if self.agent is None:
            return {"status": "unavailable", "action_executed": action}
        return self.agent.coordinate(action, dict(context or {}))

    def instruct(self, action: str, context: Any = None):
        return self.coordinate(action, context)

    def verify(self, result: Any):
        if isinstance(result, dict):
            return {"verified": result.get("status") in {"success", "accepted", "completed", "ok"}, "result": result}
        return {"verified": False, "result": result}
