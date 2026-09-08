"""Deterministic ROUTE -> INSTRUCT -> VERIFY -> RESULT orchestration."""
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time


class ProtocolError(RuntimeError):
    """Raised when a protocol stage cannot complete safely."""


@dataclass
class ProtocolEvent:
    operation: str
    status: str
    payload: Dict[str, Any] = field(default_factory=dict)


class QProtocol:
    """Execute the Q-lang coordination protocol as explicit first-class stages.

    ROUTE chooses the execution target, INSTRUCT delegates the action, VERIFY
    validates the instruction response, and RESULT seals the execution record.
    """

    VERSION = "1.0"

    def __init__(self, instructor: Optional[Callable[[str, Dict[str, Any]], Dict[str, Any]]] = None):
        self.instructor = instructor
        self.events: List[ProtocolEvent] = []

    def _emit(self, operation: str, status: str, **payload):
        event = ProtocolEvent(operation, status, payload)
        self.events.append(event)
        return event

    def route(self, action: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not isinstance(action, str) or not action.strip():
            raise ProtocolError("ROUTE requires a non-empty action")
        ctx = dict(context or {})
        target = ctx.get("agent") or "default-agent"
        route = {"protocol": self.VERSION, "stage": "ROUTE", "target": target, "action": action}
        self._emit("ROUTE", "ok", **route)
        return route

    def instruct(self, route: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = dict(context or {})
        payload.update({"route": route, "protocol": self.VERSION, "stage": "INSTRUCT"})
        if self.instructor is None:
            response = {"status": "accepted", "action_executed": route["action"], "target": route["target"]}
        else:
            response = self.instructor(route["action"], payload)
            if not isinstance(response, dict):
                raise ProtocolError("INSTRUCT adapter must return a dictionary")
        self._emit("INSTRUCT", "ok", response=response)
        return response

    def verify(self, route: Dict[str, Any], instruction: Dict[str, Any]) -> Dict[str, Any]:
        success = instruction.get("status") in {"success", "accepted", "completed", "ok"}
        verification = {
            "protocol": self.VERSION,
            "stage": "VERIFY",
            "verified": success,
            "route": route,
            "instruction": instruction,
        }
        self._emit("VERIFY", "ok" if success else "failed", **verification)
        if not success:
            raise ProtocolError(f"VERIFY failed for action: {route['action']}")
        return verification

    def result(self, route: Dict[str, Any], instruction: Dict[str, Any], verification: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            "protocol": self.VERSION,
            "stage": "RESULT",
            "status": "completed" if verification["verified"] else "failed",
            "action": route["action"],
            "target": route["target"],
            "instruction": instruction,
            "verification": verification,
            "timestamp": time.time(),
        }
        self._emit("RESULT", result["status"], **result)
        return result

    def execute(self, action: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run the complete ROUTE -> INSTRUCT -> VERIFY -> RESULT pipeline."""
        self.events.clear()
        route = self.route(action, context)
        instruction = self.instruct(route, context)
        verification = self.verify(route, instruction)
        return self.result(route, instruction, verification)
