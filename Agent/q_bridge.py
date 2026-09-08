"""Bridge between Q-lang semantic operations and the existing agent engine."""
from typing import Any

try:
    from Agent.agent import QLangAgentEngine
except ImportError:
    QLangAgentEngine = None


class QAgentBridge:
    """Expose a stable semantic interface for QRuntime.

    The bridge deliberately delegates to the existing agent layer. It does not
    invent MCP calls or execute arbitrary external tools by itself.
    """

    def __init__(self, agent=None):
        self.agent = agent or (QLangAgentEngine() if QLangAgentEngine else None)

    def coordinate(self, action: str, context: Any = None):
        if self.agent is None:
            return {"status": "unavailable", "action": action}
        return self.agent.coordinate(action, context or {})

    def instruct(self, action: str, context: Any = None):
        return self.coordinate(action, context)

    def verify(self, result: Any):
        return {"verified": True, "result": result}
