"""Execution bridge for Q-lang's semantic directive protocol."""
from typing import Any, Callable, Dict, Optional

from Core.directives import DeepSemanticProcessor
from Core.q_core import ObjectRegistry
from Core.q_directive_parser import DirectiveParser


class SemanticRuntime:
    def __init__(self, executor: Optional[Callable[[Dict[str, Any]], Any]] = None):
        self.registry = ObjectRegistry()
        self.processor = DeepSemanticProcessor(self.registry)
        self.parser = DirectiveParser()
        self.executor = executor or self._default_executor
        self.state: Dict[str, Any] = {}

    def route(self, ir) -> Dict[str, Any]:
        """Select a capability. Routing never performs execution."""
        capability = ir.capabilities[0] if ir.capabilities else "q.default"
        return {"capability": capability, "intent": ir.intent}

    def instruct(self, ir, route: Dict[str, Any]) -> Dict[str, Any]:
        return {"capability": route["capability"], "intent": ir.intent,
                "subject": ir.subject, "operations": list(ir.operations)}

    def execute(self, instruction: Dict[str, Any]) -> Any:
        return self.executor(instruction)

    def verify(self, instruction: Dict[str, Any], observation: Any) -> Dict[str, Any]:
        ok = observation is not None
        return {"verified": ok, "evidence": observation,
                "postconditions": ["execution returned an observation"]}

    def result(self, ir, route, instruction, observation, verification) -> Dict[str, Any]:
        return {"status": "success" if verification["verified"] else "failure",
                "intent": ir.intent, "route": route, "instruction": instruction,
                "observation": observation, "verification": verification}

    def learn(self, result: Dict[str, Any]) -> None:
        # Only verified results become trusted knowledge.
        if result["verification"]["verified"]:
            self.processor.knowledge.append({"result": result, "status": "verified"})

    def run(self, source: str) -> Dict[str, Any]:
        directive = self.parser.parse(source)
        ir = self.processor.synthesize(directive)
        route = self.route(ir)
        instruction = self.instruct(ir, route)
        if not directive.execution:
            return {"phase": "SEMANTIC", "ir": ir.to_dict(), "route": route}
        observation = self.execute(instruction)
        verification = self.verify(instruction, observation)
        result = self.result(ir, route, instruction, observation, verification)
        self.state["last_result"] = result
        self.learn(result)
        return result

    @staticmethod
    def _default_executor(instruction: Dict[str, Any]) -> Dict[str, Any]:
        return {"executed": True, "capability": instruction["capability"],
                "intent": instruction["intent"], "subject": instruction["subject"]}
